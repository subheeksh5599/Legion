from __future__ import annotations

import enum
from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Optional
from uuid import uuid4


class Severity(str, enum.Enum):
    CRITICAL = "critical"
    HIGH = "high"
    MEDIUM = "medium"
    LOW = "low"
    INFO = "info"


class VulnType(str, enum.Enum):
    PROMPT_INJECTION = "prompt_injection"
    AUTH_BYPASS = "auth_bypass"
    SQL_INJECTION = "sql_injection"
    COMMAND_INJECTION = "command_injection"
    XSS = "xss"
    HARDCODED_SECRET = "hardcoded_secret"
    PATH_TRAVERSAL = "path_traversal"
    DATA_EXFILTRATION = "data_exfiltration"
    INSECURE_DESERIALIZATION = "insecure_deserialization"
    MISSING_AUTH = "missing_auth"
    RACE_CONDITION = "race_condition"


class ScanStatus(str, enum.Enum):
    PENDING = "pending"
    SCANNING = "scanning"
    EXPLOITING = "exploiting"
    PATCHING = "patching"
    COMPLETE = "complete"
    FAILED = "failed"


class AgentRole(str, enum.Enum):
    SCANNER = "scanner"
    EXPLOITER = "exploiter"
    PATCHER = "patcher"
    ORCHESTRATOR = "orchestrator"


@dataclass
class Finding:
    vuln_type: VulnType
    severity: Severity
    title: str
    id: str = field(default_factory=lambda: uuid4().hex[:12])
    description: str = ""
    file_path: str = ""
    line_number: int = 0
    line_content: str = ""
    evidence: str = ""
    remediation: str = ""
    cwe: str = ""
    confidence: float = 0.0
    detected_by: AgentRole = AgentRole.SCANNER
    confirmed: bool = False
    timestamp: str = field(default_factory=lambda: datetime.now(timezone.utc).isoformat())


@dataclass
class ScanReport:
    id: str = field(default_factory=lambda: uuid4().hex[:16])
    target: str = ""
    status: ScanStatus = ScanStatus.PENDING
    findings: list[Finding] = field(default_factory=list)
    total_files: int = 0
    total_lines: int = 0
    scan_duration_ms: int = 0
    score: float = 0.0
    subnet_consensus: Optional[dict] = None
    started_at: str = ""
    completed_at: str = ""
    agents_deployed: int = 0


@dataclass
class ExploitResult:
    finding_id: str
    success: bool
    payload: str = ""
    response: str = ""
    evidence: str = ""


@dataclass
class PatchResult:
    finding_id: str
    patch: str = ""
    diff: str = ""
    verified: bool = False
