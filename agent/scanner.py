"""
Scanner Agent - Identifies vulnerabilities in source code using pattern matching
and heuristic analysis.
"""

from __future__ import annotations

import hashlib
import os
import re
from dataclasses import dataclass
from datetime import datetime, timezone

from .models import AgentRole, Finding, ScanReport, ScanStatus, Severity
from .patterns import PATTERNS, get_patterns_for_lang


@dataclass
class ScanResult:
    findings: list[Finding]
    files_analyzed: int
    lines_analyzed: int


class ScannerAgent:
    """
    Scans source code for known vulnerability patterns.

    Three detection layers:
    1. Fast regex match against known patterns
    2. Context heuristics (nearby code analysis)
    3. Confidence scoring based on match quality
    """

    def __init__(self, name: str = "scanner-01"):
        self.name = name
        self.role = AgentRole.SCANNER

    def scan_directory(self, path: str) -> ScanReport:
        """
        Recursively scan a directory for vulnerabilities.
        Returns a complete ScanReport with all findings.
        """
        report = ScanReport(
            target=os.path.abspath(path),
            status=ScanStatus.SCANNING,
            started_at=datetime.now(timezone.utc).isoformat(),
            agents_deployed=1,
        )

        all_findings: list[Finding] = []
        total_files = 0
        total_lines = 0

        for root, _, files in os.walk(path):
            if self._should_skip_dir(root):
                continue

            for filename in files:
                if not self._is_scannable(filename):
                    continue

                filepath = os.path.join(root, filename)
                try:
                    with open(filepath, "r", encoding="utf-8", errors="ignore") as f:
                        content = f.read()
                        lines = content.split("\n")
                        total_files += 1
                        total_lines += len(lines)

                        findings = self._scan_file(filepath, content, lines)
                        all_findings.extend(findings)
                except (OSError, UnicodeDecodeError):
                    continue

        report.findings = self._deduplicate(all_findings)
        report.total_files = total_files
        report.total_lines = total_lines
        report.status = ScanStatus.COMPLETE
        report.completed_at = datetime.now(timezone.utc).isoformat()
        report.score = self._calculate_score(report.findings)

        return report

    def scan_file(self, filepath: str) -> list[Finding]:
        """Scan a single file for vulnerabilities."""
        try:
            with open(filepath, "r", encoding="utf-8", errors="ignore") as f:
                content = f.read()
                lines = content.split("\n")
                return self._scan_file(filepath, content, lines)
        except (OSError, UnicodeDecodeError):
            return []

    def scan_snippet(self, code: str, language: str = "python") -> list[Finding]:
        """Scan a code snippet for vulnerabilities."""
        lines = code.split("\n")
        ext_map = {"python": ".py", "javascript": ".js", "typescript": ".ts", "go": ".go"}
        ext = ext_map.get(language, ".py")
        return self._scan_file(f"<snippet>{ext}", code, lines)

    def _scan_file(self, filepath: str, content: str, lines: list[str]) -> list[Finding]:
        findings: list[Finding] = []
        ext = os.path.splitext(filepath)[1].lower()
        patterns = get_patterns_for_lang(ext)

        for pattern in patterns:
            for match in re.finditer(pattern.regex, content, re.IGNORECASE | re.MULTILINE):
                line_num = content[: match.start()].count("\n") + 1
                line_content = lines[line_num - 1] if line_num <= len(lines) else ""

                confidence = self._calculate_confidence(pattern, match, lines, line_num)
                if confidence < 0.3:
                    continue

                findings.append(
                    Finding(
                        vuln_type=pattern.vuln_type,
                        severity=pattern.severity,
                        title=pattern.name,
                        description=pattern.description,
                        file_path=filepath,
                        line_number=line_num,
                        line_content=line_content.strip(),
                        evidence=match.group(0).strip()[:200],
                        remediation=pattern.remediation,
                        cwe=pattern.cwe,
                        confidence=round(confidence, 2),
                        detected_by=self.role,
                    )
                )

        return findings

    def _calculate_confidence(
        self, pattern: "Pattern", match: re.Match, lines: list[str], line_num: int
    ) -> float:
        """Calculate confidence score (0.0-1.0) for a regex match."""
        confidence = 0.5

        matched_text = match.group(0).lower()

        # Boost: presence of user-input indicators
        if any(
            word in matched_text
            for word in ["request", "params", "body", "input", "args", "user", "query"]
        ):
            confidence += 0.15

        # Boost: matches near imports (file is actually using the vulnerable API)
        # Boost: in production-like configs
        if any(
            word in matched_text
            for word in ["debug", "production", "deploy", "admin", "password", "secret"]
        ):
            confidence += 0.1

        # Penalty: found inside comments or test files
        before = lines[line_num - 1].strip() if line_num > 0 else ""
        if before.startswith("#") or before.startswith("//") or before.startswith("--"):
            confidence -= 0.3
        if "test" in matched_text or "example" in matched_text:
            confidence -= 0.1
        if matched_text.count("mock") > 0 or matched_text.count("dummy") > 0:
            confidence -= 0.2

        # Penalty: in .env.example or .sample files
        file_ext = os.path.splitext(getattr(pattern, "file_extensions", [""])[0])[1]
        if ".example" in match.string or ".sample" in match.string or ".test" in match.string:
            confidence -= 0.25

        return max(0.0, min(1.0, confidence))

    def _deduplicate(self, findings: list[Finding]) -> list[Finding]:
        """Remove duplicate findings (same type, same file, adjacent lines)."""
        seen: set[str] = set()
        unique: list[Finding] = []
        for f in findings:
            key = f"{f.vuln_type.value}:{f.file_path}:{f.line_number // 5}"
            if key not in seen:
                seen.add(key)
                unique.append(f)
        return sorted(unique, key=lambda x: (x.severity != Severity.CRITICAL, x.severity != Severity.HIGH, x.line_number))

    def _is_scannable(self, filename: str) -> bool:
        scannable = {
            ".py", ".js", ".ts", ".jsx", ".tsx", ".go", ".rb", ".php",
            ".java", ".rs", ".swift", ".kt", ".c", ".cpp", ".h", ".hpp",
            ".yaml", ".yml", ".toml", ".json", ".sol", ".sql",
            ".sh", ".bash", ".env",
        }
        return os.path.splitext(filename)[1].lower() in scannable

    def _should_skip_dir(self, path: str) -> bool:
        skip = {
            "node_modules",
            ".git",
            "__pycache__",
            ".next",
            "venv",
            ".venv",
            "env",
            "dist",
            "build",
            "target",
            ".idea",
            ".vscode",
            "vendor",
            ".tox",
            "egg-info",
            ".eggs",
        }
        return os.path.basename(path) in skip

    def _calculate_score(self, findings: list[Finding]) -> float:
        """Calculate overall security score (0-100)."""
        if not findings:
            return 100.0

        weights = {
            Severity.CRITICAL: 25,
            Severity.HIGH: 15,
            Severity.MEDIUM: 8,
            Severity.LOW: 3,
            Severity.INFO: 1,
        }

        penalty = sum(weights.get(f.severity, 0) * f.confidence for f in findings)
        return max(0.0, round(100.0 - penalty, 1))
