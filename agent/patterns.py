"""
Vulnerability patterns used by the Scanner agent.

Each pattern represents a known vulnerability class with detection
rules, severity mapping, and suggested remediation.
"""

from __future__ import annotations

import re
from dataclasses import dataclass

from .models import Severity, VulnType


@dataclass
class Pattern:
    vuln_type: VulnType
    severity: Severity
    cwe: str
    name: str
    description: str
    regex: str
    file_extensions: list[str]
    remediation: str


PATTERNS: list[Pattern] = [
    # === Prompt Injection ===
    Pattern(
        vuln_type=VulnType.PROMPT_INJECTION,
        severity=Severity.CRITICAL,
        cwe="CWE-931",
        name="Unsanitized LLM input concatenation",
        description="User input is directly concatenated into LLM prompts without sanitization, allowing prompt injection attacks.",
        regex=r'(?:system_prompt|prompt|messages)\s*(?:\[|=|\.append)\s*(?:[^.]*?)(?:\+|f["\']|\.format|%s|%\(|Template\(|render_template)',
        file_extensions=[".py", ".js", ".ts", ".jsx", ".tsx"],
        remediation="Never concatenate user input directly into system prompts. Use structured API parameters. Validate and sanitize all user-controlled input before passing to LLM.",
    ),
    Pattern(
        vuln_type=VulnType.PROMPT_INJECTION,
        severity=Severity.HIGH,
        cwe="CWE-931",
        name="LLM tool call with unsanitized user input",
        description="User input flows into LLM tool/function calls without validation, enabling indirect prompt injection via tools.",
        regex=r'(?:tools|functions|tool_calls)\s*(?:\[|=)\s*(?:[^)]*?)(?:request\.|event\.|body\[|params\[|args\[)',
        file_extensions=[".py", ".js", ".ts", ".go"],
        remediation="Validate tool arguments against expected schemas. Never pass raw user input directly into tool parameters. Implement allowlists for tool execution.",
    ),
    # === Auth Bypass ===
    Pattern(
        vuln_type=VulnType.AUTH_BYPASS,
        severity=Severity.CRITICAL,
        cwe="CWE-306",
        name="Missing authentication on sensitive endpoint",
        description="Protected routes lack authentication middleware or decorators, allowing unauthorized access.",
        regex=r'(?:router\.(?:get|post|put|delete|patch)|@app\.(?:route|get|post)|@router\.(?:get|post))[^@]*(?!.*(?:@login_required|@require_auth|authenticate|@jwt_required|protected\b|middleware))',
        file_extensions=[".py", ".js", ".ts"],
        remediation="Apply authentication middleware to ALL routes by default. Use deny-by-default access control. Review every route for auth decorators.",
    ),
    Pattern(
        vuln_type=VulnType.AUTH_BYPASS,
        severity=Severity.CRITICAL,
        cwe="CWE-287",
        name="JWT verification disabled or weakened",
        description="JWT token verification is set to skip signature validation or uses weak/none algorithms.",
        regex=r'(?:verify_signature\s*=\s*False|verify\s*=\s*False|algorithms\s*=\s*\[["\']none["\']|decode\([^)]*?options\s*=\s*\{[^}]*?"verify_signature"[^}]*?False)',
        file_extensions=[".py", ".js", ".ts"],
        remediation="Always verify JWT signatures. Use only strong algorithms (RS256, ES256, HS256 with 256+ bit keys). Never accept 'none' algorithm.",
    ),
    # === SQL Injection ===
    Pattern(
        vuln_type=VulnType.SQL_INJECTION,
        severity=Severity.CRITICAL,
        cwe="CWE-89",
        name="SQL query built with string concatenation",
        description="SQL queries are constructed using string formatting or concatenation with user input, enabling SQL injection.",
        regex=r'(?:execute|query|raw)\s*\(\s*(?:f["\']|[^)]*?%s|[^)]*?\.format|[^)]*?\+\s*(?:request|params|body|input|args))',
        file_extensions=[".py", ".js", ".ts", ".go", ".rb", ".php"],
        remediation="Use parameterized queries or ORM methods for ALL database operations. Never concatenate user input into SQL strings.",
    ),
    Pattern(
        vuln_type=VulnType.SQL_INJECTION,
        severity=Severity.HIGH,
        cwe="CWE-89",
        name="Raw SQL with user-controlled identifiers",
        description="Table or column names from user input used in raw SQL queries.",
        regex=r'(?:rawQuery|raw\(|sql\s*=\s*`[^`]*\$\{|SELECT.*FROM.*\{|INSERT.*VALUES.*\{)',
        file_extensions=[".js", ".ts", ".py"],
        remediation="Validate table/column names against allowlists. Never use user input for schema identifiers without strict validation.",
    ),
    # === Command Injection ===
    Pattern(
        vuln_type=VulnType.COMMAND_INJECTION,
        severity=Severity.CRITICAL,
        cwe="CWE-78",
        name="OS command built with user input",
        description="System commands are constructed with unsanitized user input, enabling arbitrary command execution.",
        regex=r'(?:os\.system|subprocess\.(?:call|run|Popen|check_output)|exec|execSync|spawn|popen|shell_exec|passthru|proc_open)\s*\(\s*[^)]*(?:f["\']|\+|\.format|request|params|body|input|args)',
        file_extensions=[".py", ".js", ".ts", ".go", ".rb", ".php", ".sh"],
        remediation="Avoid shell commands with user input. Use subprocess.run with shell=False and argument lists. If unavoidable, use shlex.quote() or equivalent.",
    ),
    # === Hardcoded Secrets ===
    Pattern(
        vuln_type=VulnType.HARDCODED_SECRET,
        severity=Severity.CRITICAL,
        cwe="CWE-798",
        name="Hardcoded API key or secret",
        description="Credentials, API keys, or secrets are embedded directly in source code.",
        regex=r'''(?:api_key|apikey|secret|SECRET|password|PASSWORD|token|TOKEN|private_key|PRIVATE_KEY)\s*[:=]\s*["'][A-Za-z0-9_\-\.]{20,}["']''',
        file_extensions=[".py", ".js", ".ts", ".go", ".rb", ".yaml", ".yml", ".env"],
        remediation="Store secrets in environment variables, a secrets manager (Vault, AWS Secrets Manager), or .env files excluded from version control.",
    ),
    Pattern(
        vuln_type=VulnType.HARDCODED_SECRET,
        severity=Severity.CRITICAL,
        cwe="CWE-798",
        name="Hardcoded private key",
        description="RSA/EC private keys, SSH keys, or certificate keys appear in source code.",
        regex=r'(?:-----BEGIN\s*(?:RSA|EC|DSA|OPENSSH)\s*PRIVATE\s*KEY-----|-----BEGIN\s*CERTIFICATE-----)',
        file_extensions=[".py", ".js", ".ts", ".go", ".pem", ".key", ".txt"],
        remediation="Never store private keys in source code. Use key management services (KMS) and load keys from secure storage at runtime.",
    ),
    # === Cross-Site Scripting ===
    Pattern(
        vuln_type=VulnType.XSS,
        severity=Severity.HIGH,
        cwe="CWE-79",
        name="Unescaped HTML output of user data",
        description="User-controlled data is rendered in HTML without escaping, enabling reflected or stored XSS.",
        regex=r'(?:dangerouslySetInnerHTML|innerHTML\s*=|\.html\(|v-html|raw\(|safe\b|Markup\(|unescape\()\s*[^;{]*(?:request|params|body|input|args|data|user)',
        file_extensions=[".js", ".ts", ".jsx", ".tsx", ".html", ".py", ".rb"],
        remediation="Use framework escaping functions. In React, never use dangerouslySetInnerHTML with user data. In Django, use autoescape. Validate and sanitize input.",
    ),
    # === Path Traversal ===
    Pattern(
        vuln_type=VulnType.PATH_TRAVERSAL,
        severity=Severity.HIGH,
        cwe="CWE-22",
        name="Unvalidated file path from user input",
        description="File operations use unsanitized user input for paths, allowing directory traversal attacks.",
        regex=r'(?:open\s*\(|readFile|read_file|File\.new|Path\.new|send_file|send_from_directory|sendFile|static)\s*\([^)]*(?:request|params|body|input|args|filename|file_path)',
        file_extensions=[".py", ".js", ".ts", ".go", ".rb"],
        remediation="Never use user input directly in file paths. Validate with os.path.basename() or pathlib. Use allowlists for accessible directories.",
    ),
    # === Data Exfiltration ===
    Pattern(
        vuln_type=VulnType.DATA_EXFILTRATION,
        severity=Severity.HIGH,
        cwe="CWE-200",
        name="Sensitive data in error responses",
        description="Error handlers or debug mode expose stack traces, environment variables, or internal state to the client.",
        regex=r'(?:debug\s*=\s*True|DEBUG\s*=\s*True|development\s*=\s*True|DEVELOPMENT\s*=\s*True|show_error_details|include_traceback|env\b.*response)',
        file_extensions=[".py", ".js", ".ts", ".go", ".rb"],
        remediation="Disable debug mode in production. Use custom error handlers that return sanitized messages. Log detailed errors server-side only.",
    ),
    # === Insecure Deserialization ===
    Pattern(
        vuln_type=VulnType.INSECURE_DESERIALIZATION,
        severity=Severity.CRITICAL,
        cwe="CWE-502",
        name="Unsafe deserialization of user data",
        description="User-controlled data is deserialized using unsafe methods that can execute arbitrary code.",
        regex=r'(?:pickle\.(?:loads?|Unpickler)|yaml\.load\s*\(|marshal\.loads?|unserialize|eval\s*\(|JSON\.parse\s*\([^)]*request|loads?\s*\(.*request)',
        file_extensions=[".py", ".js", ".ts", ".rb"],
        remediation="Never deserialize user-controlled data. Use safe serializers (JSON, msgpack). If pickle/yaml.load is required, use yaml.safe_load() or restrict pickle to trusted data only.",
    ),
    # === Missing Authorization ===
    Pattern(
        vuln_type=VulnType.MISSING_AUTH,
        severity=Severity.HIGH,
        cwe="CWE-862",
        name="Missing authorization check on resource access",
        description="Endpoints that access user-specific resources don't verify the requesting user owns the resource.",
        regex=r'(?:@router\.(?:get|post|put|delete)|def\s+\w+)\s*\([^)]*id\b[^)]*\)\s*:.*(?!.*(?:current_user|request\.user|g\.user|owner_id\s*==|user_id\s*==\s*request))',
        file_extensions=[".py", ".js", ".ts"],
        remediation="Always verify the authenticated user has permission to access the requested resource. Check ownership before returning data.",
    ),
]


def get_patterns_for_lang(extension: str) -> list[Pattern]:
    return [p for p in PATTERNS if extension in p.file_extensions or "*" in p.file_extensions]


def get_patterns_by_type(vuln_type: VulnType) -> list[Pattern]:
    return [p for p in PATTERNS if p.vuln_type == vuln_type]
