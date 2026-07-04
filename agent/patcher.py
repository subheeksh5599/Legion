"""
Patcher Agent - Generates fixes for confirmed vulnerabilities.

Produces concrete patches with line-level diffs for each confirmed finding.
"""

from __future__ import annotations

import difflib
import os
from dataclasses import dataclass, field

from .models import AgentRole, Finding, PatchResult, VulnType


@dataclass
class PatchTemplate:
    vuln_type: VulnType
    description: str
    before_template: str
    after_template: str


PATCH_TEMPLATES: list[PatchTemplate] = [
    PatchTemplate(
        vuln_type=VulnType.PROMPT_INJECTION,
        description="Replace direct prompt concatenation with structured message format",
        before_template="prompt = system_prompt + \"\\nUser: \" + user_input",
        after_template=(
            "messages = [\n"
            '    {"role": "system", "content": system_prompt},\n'
            '    {"role": "user", "content": user_input}\n'
            "]"
        ),
    ),
    PatchTemplate(
        vuln_type=VulnType.SQL_INJECTION,
        description="Replace string-formatted SQL with parameterized query",
        before_template='cursor.execute(f"SELECT * FROM users WHERE id = {user_id}")',
        after_template='cursor.execute("SELECT * FROM users WHERE id = ?", (user_id,))',
    ),
    PatchTemplate(
        vuln_type=VulnType.COMMAND_INJECTION,
        description="Replace shell command with subprocess.run using argument list",
        before_template='os.system(f"ping {hostname}")',
        after_template='subprocess.run(["ping", "-c", "1", hostname], check=True)',
    ),
    PatchTemplate(
        vuln_type=VulnType.XSS,
        description="Replace dangerouslySetInnerHTML with safe rendering",
        before_template="<div dangerouslySetInnerHTML={{ __html: userContent }} />",
        after_template=(
            "<div>{sanitizeHtml(userContent)}</div>\n\n"
            "// Add: import DOMPurify from 'dompurify';\n"
            "// const sanitizeHtml = (dirty) => ({ __html: DOMPurify.sanitize(dirty) });"
        ),
    ),
    PatchTemplate(
        vuln_type=VulnType.HARDCODED_SECRET,
        description="Replace hardcoded secret with environment variable",
        before_template='API_KEY = "sk-abc123def456"',
        after_template='API_KEY = os.environ.get("API_KEY")',
    ),
    PatchTemplate(
        vuln_type=VulnType.AUTH_BYPASS,
        description="Add authentication decorator to unprotected endpoint",
        before_template="@router.get(\"/admin/users\")\ndef get_users():",
        after_template="@router.get(\"/admin/users\")\n@require_auth\ndef get_users():",
    ),
    PatchTemplate(
        vuln_type=VulnType.PATH_TRAVERSAL,
        description="Add path validation to file operations",
        before_template='with open(user_path, "r") as f:',
        after_template=(
            'safe_path = os.path.join(BASE_DIR, os.path.basename(user_path))\n'
            'if not os.path.realpath(safe_path).startswith(BASE_DIR):\n'
            '    raise ValueError("Invalid path")\n'
            'with open(safe_path, "r") as f:'
        ),
    ),
]


class PatcherAgent:
    """
    Generates patches for confirmed vulnerabilities.

    Produces concrete fixes with before/after code and unified diffs.
    """

    def __init__(self, name: str = "patcher-01"):
        self.name = name
        self.role = AgentRole.PATCHER

    def generate_patch(self, finding: Finding) -> PatchResult:
        """
        Generate a patch for a single finding.
        Returns PatchResult with the fix and verification status.
        """
        template = self._find_template(finding)
        if not template:
            return PatchResult(
                finding_id=finding.id,
                patch=f"# Manual fix needed for {finding.vuln_type.value}",
                verified=False,
            )

        patch = self._build_patch(finding, template)
        diff = self._generate_diff(finding, template)
        verified = self._verify_patch(finding, template)

        return PatchResult(
            finding_id=finding.id,
            patch=patch,
            diff=diff,
            verified=verified,
        )

    def generate_patches(self, findings: list[Finding]) -> list[PatchResult]:
        """Generate patches for multiple findings."""
        return [self.generate_patch(f) for f in findings]

    def _find_template(self, finding: Finding) -> PatchTemplate | None:
        for t in PATCH_TEMPLATES:
            if t.vuln_type == finding.vuln_type:
                return t
        return None

    def _build_patch(self, finding: Finding, template: PatchTemplate) -> str:
        """Build a human-readable patch string."""
        return (
            f"--- {finding.file_path}:{finding.line_number}\n"
            f"+++ {finding.file_path}:{finding.line_number} (fixed)\n"
            f"@@ Fix: {template.description} @@\n\n"
            f"  Before:\n"
            f"    {finding.line_content}\n\n"
            f"  After:\n"
            f"    {template.after_template}\n\n"
            f"  CWE: {finding.cwe}\n"
            f"  Severity: {finding.severity.value}\n"
            f"  Verification: {'PASS' if self._verify_patch(finding, template) else 'NEEDS REVIEW'}"
        )

    def _generate_diff(self, finding: Finding, template: PatchTemplate) -> str:
        """Generate a unified diff for the patch."""
        before_lines = finding.line_content.split("\n")
        after_lines = template.after_template.split("\n")

        diff = difflib.unified_diff(
            before_lines,
            after_lines,
            fromfile=f"a/{finding.file_path}",
            tofile=f"b/{finding.file_path}",
            lineterm="",
        )
        return "\n".join(diff)

    def _verify_patch(self, finding: Finding, template: PatchTemplate) -> bool:
        """
        Verify that the patch would fix the vulnerability.
        Simple heuristic: check if the after_template no longer matches
        the vulnerability pattern.
        """
        # Simplified verification - in production this would use static analysis
        import re

        from .patterns import PATTERNS

        for pattern in PATTERNS:
            if pattern.vuln_type == finding.vuln_type:
                if re.search(pattern.regex, template.after_template, re.IGNORECASE):
                    return False

        return True
