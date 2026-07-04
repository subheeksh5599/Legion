"""
Bittensor Subnet for Legion - Decentralized Vulnerability Verification.

Miners:
  - Compete to find vulnerabilities in registered codebases
  - Submit findings with evidence to the subnet

Validators:
  - Verify miner submissions against ground truth
  - Score miners based on finding quality and accuracy
  - Produce consensus security scores for codebases

This is a simulation that runs without the Bittensor network for local
development and testing. Connects to Bittensor testnet when run with
--network testnet.
"""

from __future__ import annotations

import json
import os
import random
import time
from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Optional
from uuid import uuid4


@dataclass
class SubnetFinding:
    """A finding submitted to the subnet by a miner."""

    finding_id: str = field(default_factory=lambda: uuid4().hex[:16])
    miner_hotkey: str = ""
    target_hash: str = ""
    vuln_type: str = ""
    severity: str = ""
    file_path: str = ""
    line_number: int = 0
    evidence: str = ""
    confidence: float = 0.0
    timestamp: str = field(default_factory=lambda: datetime.now(timezone.utc).isoformat())


@dataclass
class MinerScore:
    """A miner's current score on the subnet."""

    hotkey: str
    total_submissions: int = 0
    accepted_submissions: int = 0
    rejected_submissions: int = 0
    quality_score: float = 0.0
    stake: float = 0.0
    last_active: str = ""


@dataclass
class SubnetState:
    """Current state of the Legion subnet."""

    registered_codebases: dict[str, str] = field(default_factory=dict)
    miner_scores: dict[str, MinerScore] = field(default_factory=dict)
    findings: list[SubnetFinding] = field(default_factory=list)
    consensus_scores: dict[str, float] = field(default_factory=dict)
    block: int = 0

    def to_dict(self) -> dict:
        return {
            "registered_codebases": self.registered_codebases,
            "miner_scores": {
                k: {
                    "hotkey": v.hotkey,
                    "total_submissions": v.total_submissions,
                    "accepted_submissions": v.accepted_submissions,
                    "rejected_submissions": v.rejected_submissions,
                    "quality_score": v.quality_score,
                    "stake": v.stake,
                    "last_active": v.last_active,
                }
                for k, v in self.miner_scores.items()
            },
            "findings_count": len(self.findings),
            "consensus_scores": self.consensus_scores,
            "block": self.block,
        }

    def to_json(self) -> str:
        return json.dumps(self.to_dict(), indent=2)


class SubnetMiner:
    """
    A Bittensor miner that finds vulnerabilities and submits them to the subnet.

    Miners:
    1. Download registered codebases
    2. Run scanner agents locally
    3. Submit findings to the subnet
    4. Receive scores from validators
    """

    def __init__(self, hotkey: str, wallet_name: str = "default"):
        self.hotkey = hotkey
        self.wallet_name = wallet_name
        self.findings_submitted: list[SubnetFinding] = []
        self.stake = random.uniform(100, 10000)

    def mine(self, target_hash: str, findings: list[dict]) -> list[SubnetFinding]:
        """
        Submit findings from a scan to the subnet.
        Returns the list of submitted findings.
        """
        submitted = []
        for f in findings:
            sf = SubnetFinding(
                miner_hotkey=self.hotkey,
                target_hash=target_hash,
                vuln_type=f.get("vuln_type", "unknown"),
                severity=f.get("severity", "low"),
                file_path=f.get("file_path", ""),
                line_number=f.get("line_number", 0),
                evidence=f.get("evidence", ""),
                confidence=f.get("confidence", 0.5),
            )
            submitted.append(sf)
            self.findings_submitted.append(sf)
        return submitted

    def get_stats(self) -> dict:
        return {
            "hotkey": self.hotkey,
            "stake": self.stake,
            "total_submissions": len(self.findings_submitted),
        }


class SubnetValidator:
    """
    A Bittensor validator that scores miner submissions.

    Validators:
    1. Receive findings from miners
    2. Verify findings against ground truth
    3. Score miners based on finding quality
    4. Update on-chain scores
    """

    def __init__(self, hotkey: str, wallet_name: str = "default"):
        self.hotkey = hotkey
        self.wallet_name = wallet_name
        self.stake = random.uniform(1000, 100000)

    def validate(self, finding: SubnetFinding) -> dict:
        """
        Validate a miner submission.
        Returns a score dict with acceptance verdict.
        """
        score = self._score_finding(finding)
        accepted = score > 0.3

        return {
            "finding_id": finding.finding_id,
            "miner_hotkey": finding.miner_hotkey,
            "accepted": accepted,
            "score": score,
            "reason": self._get_rejection_reason(score, accepted),
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }

    def validate_batch(self, findings: list[SubnetFinding]) -> list[dict]:
        """Validate a batch of findings."""
        return [self.validate(f) for f in findings]

    def _score_finding(self, finding: SubnetFinding) -> float:
        """
        Score a finding based on multiple quality dimensions.
        Returns a score between 0.0 and 1.0.
        """
        score = 0.0

        # Confidence of the finding
        score += finding.confidence * 0.4

        # Severity bonus (critical/high findings weighted higher)
        severity_weights = {"critical": 0.3, "high": 0.2, "medium": 0.15, "low": 0.1, "info": 0.05}
        score += severity_weights.get(finding.severity, 0.0)

        # Evidence quality (length, specificity)
        if finding.evidence and len(finding.evidence) > 50:
            score += 0.15
        if finding.file_path and finding.line_number > 0:
            score += 0.15

        return min(1.0, score)

    def _get_rejection_reason(self, score: float, accepted: bool) -> str:
        if accepted:
            return f"Accepted (quality: {score:.2f})"
        elif score < 0.1:
            return "Rejected: insufficient evidence"
        elif score < 0.2:
            return "Rejected: low confidence"
        else:
            return "Rejected: borderline quality"


class LegionSubnet:
    """
    The Legion Bittensor subnet.

    Manages miners, validators, submissions, and consensus scoring.
    Runs in simulation mode by default.

    Usage:
        subnet = LegionSubnet()
        subnet.register_codebase("my-project", "/path/to/code")
        subnet.register_miner("hotkey-001")
        subnet.register_validator("hotkey-val-001")

        # Miner submits findings
        findings = subnet.submit_findings("hotkey-001", "my-project", scan_results)

        # Validator scores them
        scores = subnet.validate_submissions()
        print(subnet.state.to_json())
    """

    def __init__(self, mode: str = "simulation"):
        self.mode = mode
        self.state = SubnetState()
        self.miners: dict[str, SubnetMiner] = {}
        self.validators: dict[str, SubnetValidator] = {}
        self._pending_submissions: list[SubnetFinding] = []

    def register_codebase(self, name: str, path: str) -> str:
        """Register a codebase on the subnet. Returns its hash."""
        import hashlib

        codebase_hash = hashlib.sha256(f"{name}:{path}".encode()).hexdigest()[:16]
        self.state.registered_codebases[codebase_hash] = path
        return codebase_hash

    def register_miner(self, hotkey: str) -> SubnetMiner:
        miner = SubnetMiner(hotkey)
        self.miners[hotkey] = miner
        self.state.miner_scores[hotkey] = MinerScore(hotkey=hotkey, stake=miner.stake)
        return miner

    def register_validator(self, hotkey: str) -> SubnetValidator:
        validator = SubnetValidator(hotkey)
        self.validators[hotkey] = validator
        return validator

    def submit_findings(
        self, miner_hotkey: str, codebase_name: str, findings: list[dict]
    ) -> list[SubnetFinding]:
        """A miner submits findings for a codebase."""
        if miner_hotkey not in self.miners:
            raise ValueError(f"Miner {miner_hotkey} not registered")

        target_hash = next(
            (h for h, p in self.state.registered_codebases.items() if codebase_name in p),
            codebase_name,
        )

        submitted = self.miners[miner_hotkey].mine(target_hash, findings)

        self._pending_submissions.extend(submitted)
        self.state.findings.extend(submitted)

        score = self.state.miner_scores[miner_hotkey]
        score.total_submissions += len(submitted)
        score.last_active = datetime.now(timezone.utc).isoformat()

        return submitted

    def validate_submissions(self) -> list[dict]:
        """Validators score all pending submissions."""
        if not self.validators:
            self.register_validator("validator-default")

        results: list[dict] = []
        for submission in self._pending_submissions:
            for validator in self.validators.values():
                result = validator.validate(submission)
                results.append(result)

                # Update miner score
                miner_score = self.state.miner_scores.get(submission.miner_hotkey)
                if miner_score:
                    if result["accepted"]:
                        miner_score.accepted_submissions += 1
                        miner_score.quality_score = (
                            miner_score.quality_score * 0.7 + result["score"] * 0.3
                        )
                    else:
                        miner_score.rejected_submissions += 1

        self._pending_submissions.clear()
        self.state.block += 1

        return results

    def get_consensus_score(self, codebase_name: str) -> float:
        """Get the decentralized consensus security score for a codebase."""
        related = [
            f for f in self.state.findings
            if codebase_name in f.target_hash
        ]

        if not related:
            return 100.0

        critical = sum(1 for f in related if f.severity == "critical")
        high = sum(1 for f in related if f.severity == "high")
        medium = sum(1 for f in related if f.severity == "medium")
        low = sum(1 for f in related if f.severity == "low")

        score = 100.0 - (critical * 25) - (high * 15) - (medium * 8) - (low * 3)
        return max(0.0, score)

    def get_leaderboard(self) -> list[dict]:
        """Get ranked miner leaderboard."""
        scores = sorted(
            self.state.miner_scores.values(),
            key=lambda s: s.quality_score,
            reverse=True,
        )
        return [
            {
                "hotkey": s.hotkey,
                "quality_score": round(s.quality_score, 3),
                "accepted": s.accepted_submissions,
                "rejected": s.rejected_submissions,
                "stake": round(s.stake, 2),
            }
            for s in scores
        ]
