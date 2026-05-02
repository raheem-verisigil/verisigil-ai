"""
VeriSigil AI — LangChain Integration Example
Run: python examples/python/langchain_integration.py
"""

from verisigil import VeriSigil

vs = VeriSigil(api_key="demo")


class SecureAgent:
    """A VeriSigil-secured agent wrapper."""

    def __init__(self, name: str, owner: str):
        self.name = name
        self._vs  = VeriSigil(api_key="demo")
        print(f"🔐 Registering '{name}' with VeriSigil...")
        self.passport = self._vs.issue_passport(
            agent_name=name, owner=owner, framework="langchain"
        )
        print(f"   ✅ DID: {self.passport.did}")

    def run(self, task: str) -> str:
        print(f"\n▶  Task: '{task}'")
        if not self._vs.verify(self.passport.agent_id):
            raise PermissionError("Identity verification failed — task blocked.")
        if not self.passport.is_trusted():
            raise PermissionError(f"Trust score {self.passport.trust_score} below 0.80.")
        print(f"   ✅ Identity verified")
        print(f"   ✅ Trust threshold met")
        return f"[VERIFIED] Task '{task}' completed by '{self.name}'"


if __name__ == "__main__":
    print("=" * 55)
    print("  VeriSigil + LangChain Integration Demo")
    print("=" * 55)

    agent = SecureAgent("market-research-agent", "research@example.com")

    result1 = agent.run("Analyse Q1 2026 AAPL earnings")
    result2 = agent.run("Generate portfolio risk report")

    print(f"\n✅ {result1}")
    print(f"✅ {result2}")
    print("\nAll tasks completed with verified identity.")
