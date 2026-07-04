"""
Legion CLI - Command-line interface for deploying red-team agents.

Usage:
    legion scan /path/to/codebase
    legion scan --file app.py
    legion subnet status
    legion subnet leaderboard
"""

from __future__ import annotations

import argparse
import json
import os
import sys
import time


def main():
    parser = argparse.ArgumentParser(
        description="Legion - Autonomous Red-Team Agents for Legacy Systems",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  legion scan /path/to/codebase      Full scan with agent swarm
  legion scan --file app.py           Scan a single file
  legion subnet status                Check subnet state
  legion subnet leaderboard           View miner rankings
  legion serve                        Start API server
        """,
    )

    subparsers = parser.add_subparsers(dest="command", help="Command to run")

    # scan command
    scan_parser = subparsers.add_parser("scan", help="Scan a codebase or file")
    scan_parser.add_argument("target", nargs="?", help="Path to codebase")
    scan_parser.add_argument("--file", "-f", help="Scan a single file")
    scan_parser.add_argument("--json", action="store_true", help="Output as JSON")
    scan_parser.add_argument("--quiet", "-q", action="store_true", help="Minimal output")

    # subnet command
    subnet_parser = subparsers.add_parser("subnet", help="Subnet operations")
    subnet_sub = subnet_parser.add_subparsers(dest="subnet_command")
    subnet_sub.add_parser("status", help="Show subnet state")
    subnet_sub.add_parser("leaderboard", help="Show miner leaderboard")

    # serve command
    subparsers.add_parser("serve", help="Start the Legion API server")

    args = parser.parse_args()

    if args.command == "scan":
        _run_scan(args)
    elif args.command == "subnet":
        _run_subnet(args)
    elif args.command == "serve":
        _run_serve()
    else:
        parser.print_help()


def _run_scan(args):
    from agent.orchestrator import AgentOrchestrator

    if args.file:
        orchestrator = AgentOrchestrator(scanner_count=1, exploiter_count=1, patcher_count=1)
        findings = orchestrator.scan_single_file(args.file)

        if args.json:
            print(json.dumps([_finding_to_dict(f) for f in findings], indent=2))
        else:
            _print_findings(findings)
        return

    if not args.target:
        print("Error: specify a target path or use --file", file=sys.stderr)
        sys.exit(1)

    target = os.path.abspath(args.target)
    if not os.path.exists(target):
        print(f"Error: {target} does not exist", file=sys.stderr)
        sys.exit(1)

    if not args.quiet:
        print(f"\n╔══════════════════════════════════════╗")
        print(f"║   LEGION - Agent Swarm Deployed       ║")
        print(f"╚══════════════════════════════════════╝")
        print(f"\nTarget: {target}")
        print(f"Agents: 2 scanners, 1 exploiter, 1 patcher")
        print(f"Status: Scanning...\n")

    start = time.time()
    orchestrator = AgentOrchestrator(scanner_count=2, exploiter_count=1, patcher_count=1)
    report = orchestrator.scan(target)
    elapsed = time.time() - start

    if args.json:
        print(json.dumps(_report_to_dict(report), indent=2))
    else:
        _print_report(report, elapsed)


def _print_findings(findings):
    if not findings:
        print("\n  ✓ No vulnerabilities detected.")
        return

    for f in findings:
        color = {"critical": "\033[91m", "high": "\033[93m", "medium": "\033[94m", "low": "\033[90m", "info": "\033[0m"}.get(f.severity.value, "")
        reset = "\033[0m"
        print(f"  {color}[{f.severity.value.upper()}]{reset} {f.title}")
        print(f"    {f.file_path}:{f.line_number}")
        print(f"    {f.evidence[:120]}")
        print()


def _print_report(report, elapsed):
    print(f"\n{'='*60}")
    print(f"  SCAN COMPLETE")
    print(f"{'='*60}")
    print(f"  Files analyzed:  {report.total_files}")
    print(f"  Lines scanned:   {report.total_lines}")
    print(f"  Vulnerabilities: {len(report.findings)}")
    print(f"  Confirmed:       {sum(1 for f in report.findings if f.confirmed)}")
    print(f"  Duration:        {elapsed:.2f}s")
    print(f"  Security Score:  {report.score}/100")
    print(f"{'='*60}\n")

    if report.findings:
        print("  FINDINGS:\n")
        for f in sorted(report.findings, key=lambda x: x.confirmed, reverse=True):
            status = "✓ CONFIRMED" if f.confirmed else "○ unconfirmed"
            color = "\033[91m" if f.severity.value == "critical" else "\033[93m" if f.severity.value == "high" else "\033[0m"
            reset = "\033[0m"
            print(f"  {color}[{f.severity.value.upper()}]{reset} {status}")
            print(f"    {f.title}")
            print(f"    {f.file_path}:{f.line_number}")
            if f.evidence:
                print(f"    Evidence: {f.evidence[:100]}")
            if f.remediation:
                print(f"    Fix: {f.remediation[:100]}")
            print()
    else:
        print("  ✓ No vulnerabilities detected.\n")


def _run_subnet(args):
    from subnet import LegionSubnet

    subnet = LegionSubnet()

    if args.subnet_command == "status":
        print(subnet.state.to_json())

    elif args.subnet_command == "leaderboard":
        leaderboard = subnet.get_leaderboard()
        print(json.dumps(leaderboard, indent=2))

    else:
        print("Available subnet commands: status, leaderboard")


def _run_serve():
    import uvicorn
    uvicorn.run("api.main:app", host="0.0.0.0", port=8000, reload=True)


def _finding_to_dict(f):
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
    }


def _report_to_dict(report):
    return {
        "id": report.id,
        "target": report.target,
        "status": report.status.value,
        "total_files": report.total_files,
        "total_lines": report.total_lines,
        "score": report.score,
        "scan_duration_ms": report.scan_duration_ms,
        "findings": [_finding_to_dict(f) for f in report.findings],
        "critical_count": sum(1 for f in report.findings if f.severity.value == "critical"),
        "high_count": sum(1 for f in report.findings if f.severity.value == "high"),
        "medium_count": sum(1 for f in report.findings if f.severity.value == "medium"),
        "low_count": sum(1 for f in report.findings if f.severity.value == "low"),
    }
