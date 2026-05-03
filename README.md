# VeriSigil AI 🔐

**The Trust Layer for Autonomous AI Agents**

[![CI](https://github.com/raheem-verisigil/verisigil-ai/actions/workflows/ci.yml/badge.svg)](https://github.com/raheem-verisigil/verisigil-ai/actions)
[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
[![Python 3.8+](https://img.shields.io/badge/python-3.8%2B-blue)](https://python.org)
[![EU AI Act Ready](https://img.shields.io/badge/EU%20AI%20Act-Ready-success)](https://verisigilai.com)

🌐 **Website:** [verisigilai.com](https://www.verisigilai.com)
✉️ **Contact:** [info@verisigilai.com](mailto:info@verisigilai.com)

---

## 🚀 Try in 10 Seconds

1. Open: https://verisigil-api-production.up.railway.app/docs
2. Click **POST /v1/passport/issue** → **Try it out** → **Execute**
3. Copy your `agent_id` from the response
4. Open: `https://verisigil-api-production.up.railway.app/verify/YOUR_AGENT_ID`
5. See `"valid": true` — real Ed25519 cryptographic proof

No account. No setup. No credit card.

---

## 🔐 Live Example — Verify a Real Agent Right Now

| | |
|---|---|
| **Agent ID** | `vsa_843cc558bae3` |
| **Verify** | https://verisigil-api-production.up.railway.app/verify/vsa_843cc558bae3 |
| **Audit Log** | https://verisigil-api-production.up.railway.app/v1/passport/vsa_843cc558bae3/audit |
| **DID Document** | https://verisigil-api-production.up.railway.app/did/vsa_843cc558bae3 |

---

## The Problem

Every AI agent running in production today has no identity. It cannot prove who it is. It can be impersonated. It can be compromised mid-execution. And from **August 2026**, deploying AI agents without certified identity and audit trails violates the EU AI Act — penalties of **€30M or 6% of global revenue**.

VeriSigil AI solves all three problems in one SDK.

---

## What VeriSigil AI Does

| Layer | What it provides | Status |
|-------|-----------------|--------|
| 🔐 **Identity Passports** | Cryptographic DID (W3C) for every agent | ✅ Live |
| 🛡️ **Security Scan Engine** | Real-time code scanning, threat detection | 🔶 Q2 2026 |
| 🧬 **Behavioral Fingerprinting** | ML-powered continuous authentication | 🔶 Q3 2026 |
| ✅ **ZK Compliance Engine** | EU AI Act, GDPR, HIPAA certification | ⬜ Post-seed |
| 🔗 **Federated Trust Network** | Decentralised verification mesh | ⬜ Post-seed |

---

## Quick Start — Python

```bash
pip install verisigil
```

```python
from verisigil import VeriSigil

vs = VeriSigil(api_key="demo")

passport = vs.issue_passport(
    agent_name="my-agent",
    owner="team@mycompany.com",
    framework="langchain",
)

print(passport.did)
print(passport.trust_score)
print(passport.compliant)
```

---

## Quick Start — JavaScript

```bash
npm install @verisigil/sdk
```

```javascript
const { VeriSigil } = require('@verisigil/sdk');
const vs = new VeriSigil({ apiKey: 'demo' });

const passport = await vs.issuePassport({
  agentName: 'my-agent',
  owner: 'team@mycompany.com',
  framework: 'openai',
});

console.log(passport.did);
console.log(passport.trustScore);
```

---

## Current Status — Building in Public

| Component | Status | Notes |
|-----------|--------|-------|
| Identity Passport API | ✅ **Live** | Ed25519 signed — demo available now |
| Cryptographic Audit Log | ✅ **Live** | Every event signed and verifiable |
| W3C DID Resolution | ✅ **Live** | Public endpoint — no auth needed |
| Security Scan Engine | 🔶 **In development** | Q2 2026 beta |
| Behavioral Fingerprinting | 🔶 **Planned** | Q3 2026 |
| ZK Compliance Engine | ⬜ **Architecture complete** | Post-seed build |
| Paying customers | ❌ **Pre-revenue** | 10 enterprise LOIs signed |

---

## EU AI Act — August 2026 Deadline

Enforcement begins **August 2026**. Penalties: **€30M or 6% of global revenue**. VeriSigil AI is designed EU AI Act-first from day one.

---

## Run the Examples

```bash
git clone https://github.com/raheem-verisigil/verisigil-ai.git
cd verisigil-ai
pip install requests
python examples/python/quickstart.py
node examples/javascript/quickstart.js
pip install pytest && pytest tests/ -v
```

---

## Roadmap

| Quarter | Milestone |
|---------|-----------|
| Q2 2026 | Passport API public launch · Security scan engine beta |
| Q3 2026 | Behavioral fingerprinting · 500 agents · $100K MRR |
| Q4 2026 | EU AI Act certification · ZK compliance · SOC 2 Type II |
| Q2 2027 | Series A · Federated trust network · 10,000 agents |

---

## License

MIT — see [LICENSE](LICENSE) for details.

---

## About

Built by Raheem Larry Babatunde, Founder & CEO.
7+ years building fraud detection systems that caught $50M+ in financial crime.
Lagos · Dubai · London · EU

**Making AI agents trustworthy by default.**

*Star ⭐ this repo if you believe every AI agent should have a verified identity.*
