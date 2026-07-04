<div align="center">

# Legion

**Autonomous red-team agents that attack your legacy code before attackers do.**

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![GitHub Stars](https://img.shields.io/github/stars/subheeksh5599/Legion?style=flat)](https://github.com/subheeksh5599/Legion/stargazers)

Built for UK AI Agent Hackathon EP5 × Conduct at Imperial College London.

</div>

<br/>

<p align="center">
  <img src="public/og-image.png" alt="Legion in action" width="800" />
</p>

<p align="center">
  <strong>If you find Legion useful, please consider giving it a ⭐</strong>
</p>

## Why Legion?

You're deploying AI agents into a 15-year-old banking system. The code has no tests, no docs, and was last touched by someone who left the company in 2012. Before you connect an agent to it, you need to know: can an attacker break this?

Or you're a compliance officer staring at a SOC 2 audit. The auditors ask: "Have you tested your agent-connected systems for prompt injection?" You have no answer.

Legion answers both questions:

- **Scans autonomously** — deploys specialized adversarial agents that probe legacy code for injection points, auth bypasses, and data leaks
- **Pins findings to lines** — every vulnerability comes with exact file path, line number, and reproduction steps
- **Scores decentralized** — a Bittensor subnet validates findings. Miners compete to discover exploits. Validators score quality. The network decides what's real
- **Generates patches** — each confirmed finding comes with a concrete fix, verified against the vulnerability pattern

**Built for** security engineers, compliance teams, and anyone responsible for legacy systems that agents are about to touch.

## Features

### Adversarial Agent Swarm

Three agent types attack in parallel: scanners find vulnerabilities, exploiters confirm them, patchers generate fixes. Every finding is cryptographically verified on Bittensor.

### Line-Level Evidence

No vague severity ratings. No false positives. Every vulnerability is pinned to the exact line of code with exploitation steps and CWE classification.

### Decentralized Scoring

A Bittensor subnet produces tamper-proof security ratings. Venice.ai TEE keeps the scoring methodology private and attestable. Solana records every audit on-chain.

<details>
<summary><strong>Supported Vulnerability Classes</strong></summary>

<br/>

**Injection:** Prompt Injection (CWE-931), SQL Injection (CWE-89), Command Injection (CWE-78)

**Authentication:** Auth Bypass (CWE-306), JWT Verification Bypass (CWE-287), Missing Authorization (CWE-862)

**Data Exposure:** Hardcoded Secrets (CWE-798), Hardcoded Private Keys (CWE-798), Sensitive Data in Errors (CWE-200)

**Client-Side:** Cross-Site Scripting (CWE-79), Unsafe Deserialization (CWE-502)

**File System:** Path Traversal (CWE-22)

**Languages:** Python, JavaScript, TypeScript, Go, Ruby, PHP, Java, Rust, Swift, C/C++, Solidity

</details>

## Quick Start

### 1. Clone & Install

```bash
git clone https://github.com/subheeksh5599/Legion.git
cd Legion
python3 -m venv .venv
source .venv/bin/activate
pip install fastapi uvicorn pytest
npm install
```

### 2. Run the Frontend

```bash
npm run dev
# → http://localhost:3000
```

### 3. Scan a Codebase

```bash
source .venv/bin/activate
python -m cli.legion scan /path/to/your/codebase
```

### 4. Start the API

```bash
source .venv/bin/activate
python -m uvicorn api.main:app --host 0.0.0.0 --port 8000
# → Dashboard: http://localhost:3000/dashboard
```

### 5. Run Tests

```bash
source .venv/bin/activate
python -m pytest tests/ -v
```

## How It Works

**Scan Pipeline:**
1. Scanner agents walk the target directory, checking every file against 15 vulnerability patterns
2. Each match gets a confidence score based on code context, sanitization layers, and input flow
3. Exploiter agents attempt to confirm high-severity findings with generated payloads
4. Patcher agents generate concrete fixes with before/after diffs

**Bittensor Subnet:**
- Miners submit findings with evidence to the subnet
- Validators score submissions on confidence, severity, evidence quality, and specificity
- Miner quality scores update continuously — better miners get more weight
- Consensus security scores are tamper-proof and verifiable on-chain

**Integrations:**

| Sponsor | Role |
|---------|------|
| **Bittensor** | Decentralized vulnerability verification subnet |
| **Venice.ai** | TEE-encrypted validator scoring |
| **Fetch.ai** | Agent orchestration via uAgents framework |
| **Solana** | On-chain audit trail with SBTs |
| **Conduct AI** | Enterprise governance dashboard |
| **Microsoft Azure** | Infrastructure and attack corpus storage |

## Architecture

```
User Request → AgentOrchestrator
                  ├── ScannerAgent (×2)  → pattern matching → Findings
                  ├── ExploiterAgent (×1) → payload generation → Confirmed
                  └── PatcherAgent (×1)   → diff generation   → Patches
                         │
                  Bittensor Subnet
                  ├── Miner      → submits findings
                  └── Validator  → scores submissions
                         │
                  FastAPI Backend  → /api/scan, /api/dashboard
                  Next.js Frontend → Landing page + Dashboard
```

## Deployed

- **Landing page:** [legion-lilac.vercel.app](https://legion-lilac.vercel.app)
- **Dashboard:** [legion-lilac.vercel.app/dashboard](https://legion-lilac.vercel.app/dashboard)
- **API:** Run locally with `python -m uvicorn api.main:app`

## License

[MIT](LICENSE)
