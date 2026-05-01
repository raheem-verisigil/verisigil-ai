"""
VeriSigil AI — Python Client
==============================
Full docs: https://docs.verisigilai.com
"""

import hashlib
import hmac
import os
import uuid
from datetime import datetime, timedelta
from typing import List, Optional

import requests

from .exceptions import (
    AuthenticationError,
    ComplianceError,
    PassportNotFoundError,
    RateLimitError,
    VeriSigilError,
)
from .passport import (
    ComplianceRecord,
    EURiskClass,
    Passport,
    PassportMetadata,
    PassportStatus,
)
from .version import __version__

DEFAULT_BASE_URL    = "https://api.verisigilai.com/v1"
DEMO_BASE_URL       = "https://api-demo.verisigilai.com/v1"
DEFAULT_TIMEOUT     = 30
DEFAULT_EXPIRY_DAYS = 365


class VeriSigil:
    """
    VeriSigil AI client — identity and security for AI agents.

    Example::

        from verisigil import VeriSigil

        vs = VeriSigil(api_key="demo")

        passport = vs.issue_passport(
            agent_name="my-trading-bot",
            owner="team@mycompany.com",
            framework="langchain",
        )

        print(passport.did)
        print(passport.trust_score)

        if vs.verify(passport.agent_id):
            print("Agent is verified and trusted")
    """

    def __init__(
        self,
        api_key: Optional[str] = None,
        base_url: Optional[str] = None,
        timeout: int = DEFAULT_TIMEOUT,
    ):
        self.api_key  = api_key or os.environ.get("VERISIGIL_API_KEY") or "demo"
        self.base_url = base_url or (
            DEMO_BASE_URL if self.api_key == "demo" else DEFAULT_BASE_URL
        )
        self.timeout  = timeout
        self._session = requests.Session()
        self._session.headers.update({
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type":  "application/json",
            "User-Agent":    f"verisigil-python/{__version__}",
        })

    def issue_passport(
        self,
        agent_name:  str,
        owner:       str,
        framework:   str = "unknown",
        runtime:     str = "python",
        version:     str = "1.0.0",
        tags:        Optional[List[str]] = None,
        expiry_days: int = DEFAULT_EXPIRY_DAYS,
    ) -> Passport:
        """
        Issue a new identity passport for an AI agent.

        Args:
            agent_name:  Name for this agent.
            owner:       Email of the accountable human owner.
            framework:   AI framework (langchain, openai, etc.)
            runtime:     Runtime environment (python, javascript, etc.)
            version:     Agent version string.
            tags:        Optional metadata tags.
            expiry_days: Passport validity in days (default 365).

        Returns:
            Passport: The issued identity passport.
        """
        if self.api_key == "demo":
            return self._demo_passport(
                agent_name, owner, framework, runtime, version, tags or [], expiry_days
            )
        payload = {
            "agent_name":  agent_name,
            "owner":       owner,
            "framework":   framework,
            "runtime":     runtime,
            "version":     version,
            "tags":        tags or [],
            "expiry_days": expiry_days,
        }
        data = self._post("/passport/issue", payload)
        return self._parse_passport(data)

    def verify(self, agent_id: str) -> bool:
        """
        Verify that an agent's passport is valid and active.

        Args:
            agent_id: The VeriSigil agent ID to verify.

        Returns:
            bool: True if the passport is valid and the agent is trusted.
        """
        if self.api_key == "demo":
            return True
        try:
            data = self._get(f"/passport/verify/{agent_id}")
            return data.get("verified", False)
        except PassportNotFoundError:
            return False

    def get_passport(self, agent_id: str) -> Passport:
        """Retrieve an existing passport by agent ID."""
        if self.api_key == "demo":
            return self._demo_passport(
                agent_name=f"agent-{agent_id[:8]}",
                owner="demo@verisigilai.com",
                agent_id=agent_id,
            )
        data = self._get(f"/passport/{agent_id}")
        return self._parse_passport(data)

    def revoke(self, agent_id: str, reason: str = "manual_revocation") -> bool:
        """
        Revoke an agent's passport immediately.

        Args:
            agent_id: The VeriSigil agent ID to revoke.
            reason:   Reason for revocation (logged to audit trail).

        Returns:
            bool: True if revocation succeeded.
        """
        if self.api_key == "demo":
            print(f"[DEMO] Passport revoked for agent {agent_id}. Reason: {reason}")
            return True
        payload = {"agent_id": agent_id, "reason": reason}
        data = self._post("/passport/revoke", payload)
        return data.get("revoked", False)

    def renew(self, agent_id: str, expiry_days: int = DEFAULT_EXPIRY_DAYS) -> Passport:
        """Renew an expiring or expired passport."""
        if self.api_key == "demo":
            return self._demo_passport(
                agent_name=f"agent-{agent_id[:8]}",
                owner="demo@verisigilai.com",
                agent_id=agent_id,
                expiry_days=expiry_days,
            )
        payload = {"agent_id": agent_id, "expiry_days": expiry_days}
        data = self._post("/passport/renew", payload)
        return self._parse_passport(data)

    def scan(self, code: str, agent_id: Optional[str] = None) -> dict:
        """
        Scan agent code for security vulnerabilities.

        Args:
            code:     The agent code to scan as a string.
            agent_id: Optional agent ID to associate scan with passport.

        Returns:
            dict: Scan results with threats, severity, and recommendations.
        """
        if self.api_key == "demo":
            return self._demo_scan(code)
        payload = {"code": code, "agent_id": agent_id}
        return self._post("/security/scan", payload)

    def check_compliance(
        self,
        agent_id:    str,
        regulations: Optional[List[str]] = None,
    ) -> dict:
        """
        Check an agent's compliance status against regulations.

        Args:
            agent_id:    The agent ID to check.
            regulations: List of regulations to check.
                         Options: ["eu_ai_act", "gdpr", "hipaa", "soc2"]

        Returns:
            dict: Compliance status per regulation.
        """
        if self.api_key == "demo":
            return {
                "eu_ai_act": {"compliant": True,  "risk_class": "LIMITED_RISK"},
                "gdpr":      {"compliant": True,  "lawful_basis": "legitimate_interest"},
                "hipaa":     {"compliant": False, "reason": "BAA required"},
                "soc2":      {"compliant": False, "reason": "Audit pending"},
            }
        payload = {
            "agent_id":    agent_id,
            "regulations": regulations or ["eu_ai_act", "gdpr", "hipaa", "soc2"],
        }
        return self._post("/compliance/check", payload)

    # ── HTTP ──────────────────────────────────────────────────

    def _get(self, path: str) -> dict:
        url = f"{self.base_url}{path}"
        try:
            resp = self._session.get(url, timeout=self.timeout)
            return self._handle_response(resp)
        except requests.exceptions.Timeout:
            raise VeriSigilError(f"Request timed out: GET {path}")
        except requests.exceptions.ConnectionError:
            raise VeriSigilError("Connection failed. Check your network.")

    def _post(self, path: str, payload: dict) -> dict:
        url = f"{self.base_url}{path}"
        try:
            resp = self._session.post(url, json=payload, timeout=self.timeout)
            return self._handle_response(resp)
        except requests.exceptions.Timeout:
            raise VeriSigilError(f"Request timed out: POST {path}")
        except requests.exceptions.ConnectionError:
            raise VeriSigilError("Connection failed. Check your network.")

    def _handle_response(self, resp: requests.Response) -> dict:
        if resp.status_code == 200:
            return resp.json()
        if resp.status_code == 401:
            raise AuthenticationError("Invalid API key. Get one free at verisigilai.com")
        if resp.status_code == 404:
            raise PassportNotFoundError("Agent passport not found.")
        if resp.status_code == 422:
            raise ComplianceError(f"Compliance check failed: {resp.json()}")
        if resp.status_code == 429:
            retry = resp.headers.get("Retry-After", 60)
            raise RateLimitError(f"Rate limit exceeded. Retry after {retry}s.")
        raise VeriSigilError(f"API error {resp.status_code}: {resp.text}")

    # ── Demo Mode ─────────────────────────────────────────────

    def _demo_passport(
        self,
        agent_name:  str,
        owner:       str,
        framework:   str = "langchain",
        runtime:     str = "python",
        version:     str = "1.0.0",
        tags:        Optional[List[str]] = None,
        expiry_days: int = DEFAULT_EXPIRY_DAYS,
        agent_id:    Optional[str] = None,
    ) -> Passport:
        _id   = agent_id or f"vsa_{uuid.uuid4().hex[:12]}"
        _slug = agent_name.lower().replace(" ", "-")
        _did  = f"did:web:verisigilai.com:agents:{_slug}-{_id[-6:]}"
        _sig  = f"DIDSig:{hmac.new(b'demo', _id.encode(), hashlib.sha256).hexdigest()[:32]}...{_id[-4:]}"

        now     = datetime.utcnow()
        expires = now + timedelta(days=expiry_days)

        return Passport(
            agent_id=_id,
            agent_name=agent_name,
            did=_did,
            owner=owner,
            status=PassportStatus.ACTIVE,
            trust_score=0.97,
            eu_risk_class=EURiskClass.LIMITED,
            compliant=True,
            signature=_sig,
            issued_at=now,
            expires_at=expires,
            metadata=PassportMetadata(
                framework=framework,
                runtime=runtime,
                version=version,
                tags=tags or [],
            ),
            compliance=ComplianceRecord(
                eu_ai_act=True,
                gdpr=True,
                hipaa=False,
                soc2=False,
                certified_at=now,
                expires_at=expires,
                certificate_id=f"cert_{uuid.uuid4().hex[:16]}",
            ),
            threats_detected=0,
            last_scan_at=now,
        )

    def _demo_scan(self, code: str) -> dict:
        threats = []
        lines   = code.split("\n")
        patterns = {
            "eval(":           ("HIGH",   "Unsafe eval() — arbitrary code execution risk"),
            "exec(":           ("HIGH",   "Unsafe exec() — arbitrary code execution risk"),
            "subprocess":      ("MEDIUM", "Subprocess call — verify input is sanitised"),
            "os.system":       ("HIGH",   "Direct OS command execution — use subprocess"),
            "pickle.load":     ("HIGH",   "Unsafe deserialisation — use JSON instead"),
            "password":        ("HIGH",   "Possible hardcoded credential — use env vars"),
            "api_key":         ("HIGH",   "Possible hardcoded API key — use env vars"),
            "secret":          ("HIGH",   "Possible hardcoded secret — use a vault"),
        }
        for i, line in enumerate(lines, 1):
            for pattern, (severity, description) in patterns.items():
                if pattern.lower() in line.lower():
                    threats.append({
                        "line":        i,
                        "severity":    severity,
                        "description": description,
                        "code":        line.strip(),
                    })
        return {
            "scan_id":      f"scan_{uuid.uuid4().hex[:12]}",
            "lines_scanned": len(lines),
            "threats":      threats,
            "threat_count": len(threats),
            "passed":       len(threats) == 0,
            "scanned_at":   datetime.utcnow().isoformat(),
            "demo":         True,
            "note": "Demo scan. Production scanning engine in development — Q2 2026.",
        }

    def __repr__(self) -> str:
        mode = "demo" if self.api_key == "demo" else "production"
        return f"<VeriSigil mode={mode} base_url={self.base_url}>"
