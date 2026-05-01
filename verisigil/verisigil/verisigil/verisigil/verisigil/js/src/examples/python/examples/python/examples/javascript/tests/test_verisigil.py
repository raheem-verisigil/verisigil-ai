"""
VeriSigil AI — Test Suite
Run: pytest tests/ -v
"""

import pytest
from datetime import datetime

from verisigil import VeriSigil, Passport, PassportStatus
from verisigil.passport import EURiskClass


@pytest.fixture
def vs():
    return VeriSigil(api_key="demo")


@pytest.fixture
def passport(vs):
    return vs.issue_passport(agent_name="test-agent", owner="test@example.com", framework="pytest")


class TestPassportIssuance:
    def test_returns_passport(self, vs):
        assert isinstance(vs.issue_passport(agent_name="a", owner="b@c.com"), Passport)

    def test_has_did(self, vs):
        p = vs.issue_passport(agent_name="a", owner="b@c.com")
        assert p.did.startswith("did:web:verisigilai.com:agents:")

    def test_status_active(self, passport):
        assert passport.status == PassportStatus.ACTIVE

    def test_trust_score_in_range(self, passport):
        assert 0.0 <= passport.trust_score <= 1.0

    def test_eu_risk_class_set(self, passport):
        assert passport.eu_risk_class in EURiskClass

    def test_has_owner(self, vs):
        p = vs.issue_passport(agent_name="a", owner="owner@co.com")
        assert p.owner == "owner@co.com"

    def test_has_issued_at(self, passport):
        assert isinstance(passport.issued_at, datetime)

    def test_expires_after_issued(self, passport):
        assert passport.expires_at > passport.issued_at

    def test_unique_ids(self, vs):
        p1 = vs.issue_passport(agent_name="a", owner="a@x.com")
        p2 = vs.issue_passport(agent_name="b", owner="b@x.com")
        assert p1.agent_id != p2.agent_id


class TestTrust:
    def test_is_trusted(self, passport):
        assert passport.is_trusted() is True

    def test_not_expired(self, passport):
        assert passport.is_expired() is False

    def test_meets_threshold(self, passport):
        assert passport.trust_score >= 0.80


class TestVerification:
    def test_verify_demo(self, vs, passport):
        assert vs.verify(passport.agent_id) is True


class TestScanning:
    def test_clean_passes(self, vs):
        r = vs.scan("def hello(): return 'hi'")
        assert r["passed"] is True

    def test_eval_detected(self, vs):
        r = vs.scan("result = eval(x)")
        assert r["threat_count"] > 0

    def test_secret_detected(self, vs):
        r = vs.scan('secret = "abc123"')
        assert r["threat_count"] > 0

    def test_has_required_fields(self, vs):
        r = vs.scan("x = 1")
        assert all(k in r for k in ["scan_id", "lines_scanned", "threats", "passed"])


class TestCompliance:
    def test_returns_dict(self, vs, passport):
        assert isinstance(vs.check_compliance(passport.agent_id), dict)

    def test_has_eu_ai_act(self, vs, passport):
        r = vs.check_compliance(passport.agent_id)
        assert "eu_ai_act" in r
        assert "compliant" in r["eu_ai_act"]


class TestSerialisation:
    def test_to_dict(self, passport):
        d = passport.to_dict()
        assert d["agent_id"] == passport.agent_id
        assert "did" in d
        assert "compliance" in d
