"""
VeriSigil AI — Quick Start Example
Run: python examples/python/quickstart.py
"""

from verisigil import VeriSigil

vs = VeriSigil(api_key="demo")

print("=" * 55)
print("  VeriSigil AI — Demo")
print("=" * 55)

# Issue passport
print("\n🔐 Issuing passport...")
passport = vs.issue_passport(
    agent_name="financial-analysis-agent",
    owner="team@example.com",
    framework="langchain",
)
print(f"   ✅ Issued!")
print(f"   DID:          {passport.did}")
print(f"   Trust Score:  {passport.trust_score}")
print(f"   EU Risk:      {passport.eu_risk_class.value}")
print(f"   Status:       {passport.status.value}")
print(f"   Expires:      {passport.expires_at.strftime('%Y-%m-%d')}")

# Verify
print("\n🛡️  Verifying...")
print(f"   {'✅ Verified' if vs.verify(passport.agent_id) else '⛔ NOT verified'}")

# Scan
print("\n🔍 Security scan...")
code = """
api_key = "sk-1234"
result = eval(user_input)
"""
results = vs.scan(code)
print(f"   Threats: {results['threat_count']}")
for t in results["threats"]:
    icon = "🔴" if t["severity"] == "HIGH" else "🟡"
    print(f"   {icon} [{t['severity']}] Line {t['line']}: {t['description']}")

# Compliance
print("\n⚖️  Compliance...")
c = vs.check_compliance(passport.agent_id)
print(f"   EU AI Act: {'✅' if c['eu_ai_act']['compliant'] else '❌'}")
print(f"   GDPR:      {'✅' if c['gdpr']['compliant'] else '❌'}")

print("\n" + "=" * 55)
print("  🚀 verisigilai.com  |  info@verisigilai.com")
print("=" * 55)
