"""
Legion test suite.

Run: python -m pytest tests/ -v
"""

import os
import tempfile
import pytest

from agent.scanner import ScannerAgent
from agent.exploiter import ExploiterAgent
from agent.patcher import PatcherAgent
from agent.orchestrator import AgentOrchestrator
from agent.models import Severity, VulnType
from subnet import LegionSubnet


class TestScanner:
    def test_scan_sql_injection(self):
        scanner = ScannerAgent()
        code = '''
import sqlite3
user_id = request.args.get("id")
query = f"SELECT * FROM users WHERE id = {user_id}"
cursor.execute(query)
'''
        findings = scanner.scan_snippet(code, "python")
        assert len(findings) > 0
        assert any("SQL" in f.title for f in findings)

    def test_scan_hardcoded_secret(self):
        scanner = ScannerAgent()
        code = '''
API_KEY = "sk-abc123def4567890abcdef"
SECRET = "my-super-secret-password-123"
'''
        findings = scanner.scan_snippet(code, "python")
        assert len(findings) > 0
        assert any(f.vuln_type == VulnType.HARDCODED_SECRET for f in findings)

    def test_scan_command_injection(self):
        scanner = ScannerAgent()
        code = '''
import os
hostname = request.form.get("host")
os.system(f"ping {hostname}")
'''
        findings = scanner.scan_snippet(code, "python")
        assert len(findings) > 0
        assert any(f.vuln_type == VulnType.COMMAND_INJECTION for f in findings)

    def test_scan_clean_code(self):
        scanner = ScannerAgent()
        code = '''
def add(a, b):
    return a + b

class Calculator:
    def multiply(self, x, y):
        return x * y
'''
        findings = scanner.scan_snippet(code, "python")
        assert len(findings) == 0

    def test_scan_prompt_injection(self):
        scanner = ScannerAgent()
        code = '''
system_prompt = "You are an assistant"
user_input = request.json.get("message")
prompt = system_prompt + "\\nUser: " + user_input
response = openai.chat(prompt)
'''
        findings = scanner.scan_snippet(code, "python")
        assert len(findings) > 0


class TestExploiter:
    def test_exploit_finding(self):
        exploiter = ExploiterAgent()
        from agent.models import Finding

        finding = Finding(
            vuln_type=VulnType.SQL_INJECTION,
            severity=Severity.CRITICAL,
            title="SQL injection test",
            file_path="/tmp/test.py",
            line_number=3,
            line_content='cursor.execute(f"SELECT * FROM users WHERE id = {user_id}")',
        )
        result = exploiter.exploit(finding)
        assert result.payload
        assert "Payload" in result.evidence or "UNCONFIRMED" in result.evidence


class TestPatcher:
    def test_generate_patch(self):
        patcher = PatcherAgent()
        from agent.models import Finding

        finding = Finding(
            vuln_type=VulnType.HARDCODED_SECRET,
            severity=Severity.CRITICAL,
            title="Hardcoded API key",
            file_path="/tmp/config.py",
            line_number=1,
            line_content='API_KEY = "sk-secret123"',
        )
        result = patcher.generate_patch(finding)
        assert "os.environ" in result.patch or "env" in result.patch.lower()


class TestOrchestrator:
    def test_orchestrator_scan(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            with open(os.path.join(tmpdir, "app.py"), "w") as f:
                f.write(
                    'API_KEY = "sk-abc123def456"\n'
                    'user_id = request.args.get("id")\n'
                    'cursor.execute(f"SELECT * FROM users WHERE id = {user_id}")\n'
                )

            orchestrator = AgentOrchestrator(scanner_count=1)
            report = orchestrator.scan(tmpdir)

            assert len(report.findings) > 0
            assert report.score < 100.0
            assert report.status.value == "complete"

    def test_empty_directory(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            orchestrator = AgentOrchestrator()
            report = orchestrator.scan(tmpdir)
            assert report.score == 100.0
            assert len(report.findings) == 0


class TestSubnet:
    def test_subnet_flow(self):
        subnet = LegionSubnet()

        subnet.register_codebase("test-project", "/tmp/test")
        subnet.register_miner("miner-01")
        subnet.register_validator("val-01")

        findings = [
            {"vuln_type": "sql_injection", "severity": "critical", "file_path": "app.py",
             "line_number": 5, "evidence": "User input in SQL query", "confidence": 0.9},
            {"vuln_type": "hardcoded_secret", "severity": "critical", "file_path": "config.py",
             "line_number": 1, "evidence": "API_KEY = 'sk-secret'", "confidence": 0.7},
        ]

        submitted = subnet.submit_findings("miner-01", "test-project", findings)
        assert len(submitted) == 2

        results = subnet.validate_submissions()
        assert len(results) == 2

        miner_score = subnet.state.miner_scores["miner-01"]
        assert miner_score.total_submissions == 2
        assert miner_score.accepted_submissions > 0

        consensus = subnet.get_consensus_score("test-project")
        assert consensus < 100.0

        leaderboard = subnet.get_leaderboard()
        assert len(leaderboard) >= 1
