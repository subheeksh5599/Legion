"""
Legion API Server - FastAPI backend for the agent swarm.

Endpoints:
  POST /api/scan          - Start a scan
  GET  /api/scan/{id}     - Get scan results
  POST /api/scan/snippet  - Scan a code snippet
  GET  /api/subnet/status - Get subnet state
  GET  /api/dashboard     - Dashboard summary
  GET  /api/health        - Health check
"""

from __future__ import annotations

import os
import sys
import uuid
from typing import Optional

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from agent.orchestrator import AgentOrchestrator
from agent.models import Finding, ScanReport, ScanStatus
from subnet import LegionSubnet

app = FastAPI(
    title="Legion API",
    description="Autonomous Red-Team Agent Swarm for Legacy Systems",
    version="1.0.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# State
active_scans: dict[str, ScanReport] = {}
subnet = LegionSubnet("simulation")
subnet.register_validator("validator-default")


class ScanRequest(BaseModel):
    target: str


class SnippetRequest(BaseModel):
    code: str
    language: str = "python"


class FindingResponse(BaseModel):
    id: str
    vuln_type: str
    severity: str
    title: str
    description: str
    file_path: str
    line_number: int
    line_content: str
    evidence: str
    remediation: str
    cwe: str
    confidence: float
    confirmed: bool


class ScanResponse(BaseModel):
    id: str
    target: str
    status: str
    score: float
    total_files: int
    total_lines: int
    scan_duration_ms: int
    agents_deployed: int
    findings: list[dict]
    critical_count: int
    high_count: int
    medium_count: int
    low_count: int


class DashboardResponse(BaseModel):
    total_scans: int
    total_vulnerabilities: int
    critical_count: int
    high_count: int
    confirmed_count: int
    average_score: float
    recent_scans: list[dict]
    subnet_status: dict
    agent_activity: dict


@app.get("/api/health")
async def health():
    return {"status": "operational", "version": "1.0.0", "agents_ready": True}


from concurrent.futures import ThreadPoolExecutor

executor = ThreadPoolExecutor(max_workers=2)


def _run_scan(report_id: str, target: str):
    orchestrator = AgentOrchestrator()
    report = orchestrator.scan(target)
    active_scans[report_id] = report

    subnet.register_codebase(target, target)
    subnet.register_miner("miner-01")
    subnet.submit_findings(
        "miner-01", target,
        [{"vuln_type": f.vuln_type.value, "severity": f.severity.value,
          "file_path": f.file_path, "line_number": f.line_number,
          "evidence": f.evidence, "confidence": f.confidence}
         for f in report.findings][:50],
    )
    subnet.validate_submissions()


@app.post("/api/scan")
async def start_scan(req: ScanRequest):
    if not os.path.exists(req.target):
        raise HTTPException(400, f"Target path does not exist: {req.target}")

    report_id = uuid.uuid4().hex[:16]
    active_scans[report_id] = ScanReport(
        id=report_id, target=req.target, status=ScanStatus.SCANNING,
    )
    executor.submit(_run_scan, report_id, req.target)
    return {"id": report_id, "target": req.target, "status": "scanning"}


@app.get("/api/scan/{scan_id}")
async def get_scan(scan_id: str):
    report = active_scans.get(scan_id)
    if not report:
        raise HTTPException(404, "Scan not found")
    return _format_report(report)


@app.post("/api/scan/snippet")
async def scan_snippet(req: SnippetRequest):
    orchestrator = AgentOrchestrator(scanner_count=1)
    findings = orchestrator.scanners[0].scan_snippet(req.code, req.language)
    return {
        "findings": [_finding_to_dict(f) for f in findings],
        "count": len(findings),
    }


@app.get("/api/subnet/status")
async def subnet_status():
    return {
        "block": subnet.state.block,
        "registered_codebases": len(subnet.state.registered_codebases),
        "active_miners": len(subnet.miners),
        "active_validators": len(subnet.validators),
        "total_findings": len(subnet.state.findings),
        "leaderboard": subnet.get_leaderboard(),
    }


@app.get("/api/dashboard")
async def dashboard():
    all_findings: list[Finding] = []
    for r in active_scans.values():
        all_findings.extend(r.findings)

    critical = sum(1 for f in all_findings if f.severity.value == "critical")
    high = sum(1 for f in all_findings if f.severity.value == "high")
    confirmed = sum(1 for f in all_findings if f.confirmed)
    avg_score = (
        sum(r.score for r in active_scans.values()) / len(active_scans)
        if active_scans
        else 100.0
    )

    return {
        "total_scans": len(active_scans),
        "total_vulnerabilities": len(all_findings),
        "critical_count": critical,
        "high_count": high,
        "confirmed_count": confirmed,
        "average_score": round(avg_score, 1),
        "recent_scans": [
            {
                "id": r.id,
                "target": r.target,
                "score": r.score,
                "findings": len(r.findings),
                "status": r.status.value,
                "duration_ms": r.scan_duration_ms,
            }
            for r in list(active_scans.values())[-10:]
        ],
        "subnet_status": subnet.state.to_dict(),
        "agent_activity": {
            "scanners_active": 2,
            "exploiters_active": 1,
            "patchers_active": 1,
            "subnet_miners": len(subnet.miners),
        },
    }


def _format_report(report: ScanReport) -> dict:
    return {
        "id": report.id,
        "target": report.target,
        "status": report.status.value,
        "score": report.score,
        "total_files": report.total_files,
        "total_lines": report.total_lines,
        "scan_duration_ms": report.scan_duration_ms,
        "agents_deployed": report.agents_deployed,
        "findings": [_finding_to_dict(f) for f in report.findings],
        "critical_count": sum(1 for f in report.findings if f.severity.value == "critical"),
        "high_count": sum(1 for f in report.findings if f.severity.value == "high"),
        "medium_count": sum(1 for f in report.findings if f.severity.value == "medium"),
        "low_count": sum(1 for f in report.findings if f.severity.value == "low"),
    }


def _finding_to_dict(f: Finding) -> dict:
    return {
        "id": f.id,
        "vuln_type": f.vuln_type.value,
        "severity": f.severity.value,
        "title": f.title,
        "description": f.description,
        "file_path": f.file_path,
        "line_number": f.line_number,
        "line_content": f.line_content,
        "evidence": f.evidence,
        "remediation": f.remediation,
        "cwe": f.cwe,
        "confidence": f.confidence,
        "confirmed": f.confirmed,
        "detected_by": f.detected_by.value,
        "timestamp": f.timestamp,
    }
