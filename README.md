# VeriSigil AI 🔐

[![CI/CD](https://github.com/raheem-verisigil/verisigil-ai/actions/workflows/ci.yml/badge.svg)](https://github.com/raheem-verisigil/verisigil-ai/actions)

**The Trust Layer for Autonomous AI Agents**

[![CI](https://github.com/raheem-verisigil/verisigil-ai/actions/workflows/ci.yml/badge.svg)](https://github.com/raheem-verisigil/verisigil-ai/actions)
[![PyPI version](https://img.shields.io/badge/pypi-v0.1.0-blue)](https://pypi.org/project/verisigil/)
[![npm version](https://img.shields.io/badge/npm-v0.1.0-red)](https://www.npmjs.com/package/@verisigil/sdk)
[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
[![Python 3.8+](https://img.shields.io/badge/python-3.8%2B-blue)](https://python.org)
[![EU AI Act Ready](https://img.shields.io/badge/EU%20AI%20Act-Ready-success)](https://verisigilai.com)

🌐 **Website:** [verisigilai.com](https://www.verisigilai.com)
📚 **Docs:** [docs.verisigilai.com](https://docs.verisigilai.com)
✉️ **Contact:** [info@verisigilai.com](mailto:info@verisigilai.com)

---

## The Problem

Every AI agent running in production today has no identity.

It cannot prove who it is. It can be impersonated. It can be compromised mid-execution. And from **August 2026**, deploying AI agents without certified identity and audit trails violates the EU AI Act — carrying penalties of **€30M or 6% of global revenue**.

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

# Free demo mode — no API key needed
vs = VeriSigil(api_key="demo")

# Issue a cryptographic identity passport
passport = vs.issue_passport(
    agent_name="financial-analysis-agent",
    owner="team@mycompany.com",
    framework="langchain",
)

print(passport.did)          # did:web:verisigilai.com:agents:financial-analysis-agent-a1b2c3
print(passport.trust_score)  # 0.97
print(passport.compliant)    # True

# Verify before granting access
if vs.verify(passport.agent_id):
    print("✅ Agent verified — safe to grant access")
else:
    print("⛔ Agent NOT verified — access blocked")

# Scan code for security threats
results = vs.scan(open("my_agent.py").read())
for threat in results["threats"]:
    print(f"[{threat['severity']}] Line {threat['line']}: {threat['description']}")

# Check EU AI Act compliance
status = vs.check_compliance(passport.agent_id)
print(status["eu_ai_act"])  # {"compliant": True, "risk_class": "LIMITED_RISK"}
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
  agentName: 'customer-support-agent',
  owner:     'ops@mycompany.com',
  framework: 'openai',
});

console.log(passport.did);         // did:web:verisigilai.com:agents:...
console.log(passport.trustScore);  // 0.97
console.log(passport.compliant);   // true

const verified = await vs.verify(passport.agentId);
console.log(verified ? '✅ Verified' : '⛔ NOT verified');
```

---

## What is a VeriSigil Passport?

```json
{
  "agent_id":     "vsa_7f3k9xab2c1d",
  "agent_name":   "financial-analysis-agent",
  "did":          "did:web:verisigilai.com:agents:financial-analysis-agent-7f3k9x",
  "owner":        "team@hedgefund.com",
  "status":       "ACTIVE",
  "trust_score":  0.97,
  "eu_risk":      "LIMITED_RISK",
  "compliant":    true,
  "issued_at":    "2026-05-01T09:00:00Z",
  "expires_at":   "2027-05-01T09:00:00Z",
  "issued_by":    "VeriSigil AI",
  "compliance": {
    "eu_ai_act":  true,
    "gdpr":       true,
    "hipaa":      false,
    "soc2":       false
  }
}
```┌─────────────────────────────────────────────────────────────┐
│                       YOUR AI AGENT                         │
│              (LangChain / AutoGPT / OpenAI / etc.)          │
└──────────────────────────┬──────────────────────────────────┘
│  import verisigil
▼
┌─────────────────────────────────────────────────────────────┐
│                    VERISIGIL AI SDK                         │
├──────────────┬───────────────────┬──────────────────────────┤
│  🔐 Identity │  🛡️ Security Scan │  ✅ Compliance Engine   │
│  Passports   │  (Q2 2026)        │  (Post-Seed)            │
│  [LIVE]      │                   │                          │
├──────────────┴───────────────────┴──────────────────────────┤
│  🧬 Behavioral Fingerprinting  │  🔗 Federated Trust Net   │
│  (Q3 2026)                     │  (Post-Seed)              │
└─────────────────────────────────────────────────────────────┘---

## Current Status — Building in Public

| Component | Status | Notes |
|-----------|--------|-------|
| Identity Passport API | ✅ **Live** | Demo available now |
| 8-Layer Architecture | ✅ **Designed** | 22 patents filed |
| Security Scan Engine | 🔶 **In development** | Q2 2026 beta |
| Behavioral Fingerprinting | 🔶 **Planned** | Q3 2026 |
| ZK Compliance Engine | ⬜ **Architecture complete** | Post-seed build |
| Federated Trust Network | ⬜ **Specification complete** | Post-seed build |
| Paying customers | ❌ **Pre-revenue** | 10 enterprise LOIs signed |

---

## Run the Examples

```bash
# Clone
git clone https://github.com/raheem-verisigil/verisigil-ai.git
cd verisigil-ai

# Python quick start (no API key needed)
pip install requests
python examples/python/quickstart.py

# LangChain integration
python examples/python/langchain_integration.py

# JavaScript quick start
node examples/javascript/quickstart.js

# Run tests
pip install pytest
pytest tests/ -v
```

---

## EU AI Act — August 2026 Deadline

The EU AI Act enforcement begins **August 2026**. Enterprises deploying AI agents without verified identity, audit trails, and compliance certification face penalties of **€30M or 6% of global revenue**.

VeriSigil AI is designed EU AI Act-first from day one.

---

## Get Your Free API Key

1. Go to [verisigilai.com](https://www.verisigilai.com)
2. Click **Get Early Access**
3. Use your key: `vs = VeriSigil(api_key="your-key-here")`

---

## Contributing

We are actively looking for:
- 🛠️ **Technical contributors** — cryptography, security, backend
- 🤝 **Technical co-founders** — Rust / Go / cryptography background
- 💡 **Design partners** — enterprises deploying agents in regulated industries

1. Fork the repo
2. Create a branch: `git checkout -b feature/your-feature`
3. Commit: `git commit -m 'Add your feature'`
4. Push: `git push origin feature/your-feature`
5. Open a Pull Request

---

## Roadmap

| Quarter | Milestone |
|---------|-----------|
| Q2 2026 | Passport API public launch · Security scan engine beta |
| Q3 2026 | Behavioral fingerprinting · 500 agents · $100K MRR |
| Q4 2026 | EU AI Act certification · ZK compliance · SOC 2 Type II |
| Q2 2027 | Series A · Federated trust network · 10,000 agents |

---

## Security

Found a vulnerability? Email [info@verisigilai.com](mailto:info@verisigilai.com) — do not open a public issue. We respond within 24 hours.

---

## License

MIT — see [LICENSE](LICENSE) for details.

---

## About

Built by [Raheem Larry Babatunde](mailto:info@verisigilai.com), Founder & CEO.
7+ years building fraud detection systems that caught $50M+ in financial crime.

Lagos · Dubai · London · EU

**Making AI agents trustworthy by default.**

---

*Star ⭐ this repo if you believe every AI agent should have a verified identity.*

---

## Architecture
