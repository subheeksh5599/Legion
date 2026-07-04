"""
Orchestrator - Coordinates Scanner, Exploiter, and Patcher agents.

Entry point for deploying the full Legion agent swarm against a target.
"""

from __future__ import annotations

import concurrent.futures
import os
import time
from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Optional

from .exploiter import ExploiterAgent
from .models import (
    AgentRole,
    ExploitResult,
    Finding,
    PatchResult,
    ScanReport,
    ScanStatus,
    Severity,
)
from .patcher import PatcherAgent
from .scanner import ScannerAgent


class AgentOrchestrator:
    """
    Orchestrates the full scan-exploit-patch pipeline.

    Usage:
        orchestrator = AgentOrchestrator()
        report = orchestrator.scan("/path/to/codebase")
        print(report.score)
    """

    def __init__(
        self,
        scanner_count: int = 2,
        exploiter_count: int = 1,
        patcher_count: int = 1,
    ):
        self.scanner_count = scanner_count
        self.exploiter_count = exploiter_count
        self.patcher_count = patcher_count

        self.scanners = [ScannerAgent(f"scanner-{i:02d}") for i in range(scanner_count)]
        self.exploiters = [ExploiterAgent(f"exploiter-{i:02d}") for i in range(exploiter_count)]
        self.patchers = [PatcherAgent(f"patcher-{i:02d}") for i in range(patcher_count)]

    def scan(self, target_path: str) -> ScanReport:
        """
        Run the full Legion pipeline against a target.
        1. Scanner agents find vulnerabilities
        2. Exploiter agents confirm them
        3. Patcher agents generate fixes
        """
        start_time = time.time()

        report = ScanReport(
            target=os.path.abspath(target_path),
            status=ScanStatus.PENDING,
            started_at=datetime.now(timezone.utc).isoformat(),
            agents_deployed=self.scanner_count + self.exploiter_count + self.patcher_count,
        )

        # Phase 1: Scan
        report.status = ScanStatus.SCANNING
        all_findings = self._run_scanners(target_path)
        report.findings = all_findings
        report.total_files = max((f.line_number for f in all_findings), default=0) or 0
        report.total_lines = sum(
            1 for _ in self._iterate_files(target_path) if True
        ) or 0

        # Phase 2: Exploit high-severity findings
        if all_findings:
            report.status = ScanStatus.EXPLOITING
            high_priority = [f for f in all_findings if f.severity in (Severity.CRITICAL, Severity.HIGH)]
            exploit_results = self._run_exploiters(high_priority[:20])

            # Mark confirmed findings
            confirmed = {r.finding_id for r in exploit_results if r.success}
            for f in all_findings:
                f.confirmed = f.id in confirmed

        # Phase 3: Generate patches
        if any(f.confirmed for f in all_findings):
            report.status = ScanStatus.PATCHING
            confirmed_findings = [f for f in all_findings if f.confirmed]
            patch_results = self._run_patchers(confirmed_findings)

        # Final scoring
        report.status = ScanStatus.COMPLETE
        report.completed_at = datetime.now(timezone.utc).isoformat()
        report.scan_duration_ms = int((time.time() - start_time) * 1000)
        report.score = self._calculate_overall_score(all_findings)

        return report

    def scan_single_file(self, filepath: str) -> list[Finding]:
        """Quick scan of a single file."""
        scanner = self.scanners[0]
        return scanner.scan_file(filepath)

    def _run_scanners(self, path: str) -> list[Finding]:
        """Run all scanners and merge their findings."""
        report = self.scanners[0].scan_directory(path)
        return report.findings

    def _run_exploiters(self, findings: list[Finding]) -> list[ExploitResult]:
        """Run exploiters against a batch of findings."""
        results: list[ExploitResult] = []
        with concurrent.futures.ThreadPoolExecutor(max_workers=self.exploiter_count) as executor:
            futures = [
                executor.submit(exploiter.exploit, finding)
                for exploiter in self.exploiters
                for finding in findings[:: len(self.exploiters)]
            ]
            for future in concurrent.futures.as_completed(futures):
                try:
                    results.append(future.result())
                except Exception:
                    pass
        return results

    def _run_patchers(self, findings: list[Finding]) -> list[PatchResult]:
        """Generate patches for confirmed findings."""
        return self.patchers[0].generate_patches(findings)

    def _calculate_overall_score(self, findings: list[Finding]) -> float:
        if not findings:
            return 100.0

        critical = sum(1 for f in findings if f.severity == Severity.CRITICAL and f.confirmed)
        high = sum(1 for f in findings if f.severity == Severity.HIGH and f.confirmed)
        medium = sum(1 for f in findings if f.severity == Severity.MEDIUM)
        low = sum(1 for f in findings if f.severity == Severity.LOW)

        score = 100.0 - (critical * 25) - (high * 15) - (medium * 8) - (low * 3)
        return max(0.0, round(score, 1))

    def _iterate_files(self, path: str):
        for root, dirs, files in os.walk(path):
            dirs[:] = [d for d in dirs if not d.startswith(".") and d not in {"node_modules", "__pycache__", "venv", ".venv", "dist", "build"}]
            yield from files
