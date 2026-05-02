"""
VeriSigil AI — Passport Model
==============================
"""

from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from typing import List, Optional


class PassportStatus(str, Enum):
    ISSUED    = "ISSUED"
    ACTIVE    = "ACTIVE"
    SUSPENDED = "SUSPENDED"
    REVOKED   = "REVOKED"
    EXPIRED   = "EXPIRED"


class EURiskClass(str, Enum):
    UNACCEPTABLE = "UNACCEPTABLE_RISK"
    HIGH         = "HIGH_RISK"
    LIMITED      = "LIMITED_RISK"
    MINIMAL      = "MINIMAL_RISK"


@dataclass
class PassportMetadata:
    framework: str
    runtime:   str
    version:   str
    tags:      List[str] = field(default_factory=list)


@dataclass
class ComplianceRecord:
    eu_ai_act:    bool = False
    gdpr:         bool = False
    hipaa:        bool = False
    soc2:         bool = False
    nist_ai_rmf:  bool = False
    certified_at: Optional[datetime] = None
    expires_at:   Optional[datetime] = None
    certificate_id: Optional[str] = None


@dataclass
class Passport:
    """
    Cryptographic identity passport for an AI agent.

    Attributes:
        agent_id:      Unique VeriSigil agent identifier
        agent_name:    Human-readable name for the agent
        did:           W3C DID — e.g. did:web:verisigilai.com:agents:abc123
        owner:         Email of the human accountable for this agent
        status:        Current passport status
        trust_score:   Float 0.0-1.0. Above 0.8 = trusted.
        eu_risk_class: EU AI Act risk classification
        compliant:     True if all required certifications are current
        signature:     Cryptographic signature (truncated for display)
        issued_at:     UTC timestamp of passport issuance
        expires_at:    UTC timestamp of passport expiry
        metadata:      Framework, runtime and version information
        compliance:    Compliance certification record
        threats_detected: Number of threats detected since issuance
        last_scan_at:  Timestamp of last security scan
    """
    agent_id:   str
    agent_name: str
    did:        str
    owner:      str
    status:      PassportStatus
    trust_score: float
    eu_risk_class: EURiskClass
    compliant:   bool
    signature:  str
    issued_at:  datetime
    expires_at: datetime
    metadata:   PassportMetadata
    compliance: ComplianceRecord
    threats_detected: int = 0
    last_scan_at: Optional[datetime] = None

    def is_trusted(self) -> bool:
        """Return True if this agent meets VeriSigil trust threshold."""
        return (
            self.status == PassportStatus.ACTIVE
            and self.trust_score >= 0.8
            and self.compliant
        )

    def is_expired(self) -> bool:
        """Return True if this passport has expired."""
        return datetime.utcnow() > self.expires_at

    def to_dict(self) -> dict:
        """Serialise passport to dictionary."""
        return {
            "agent_id":         self.agent_id,
            "agent_name":       self.agent_name,
            "did":              self.did,
            "owner":            self.owner,
            "status":           self.status.value,
            "trust_score":      self.trust_score,
            "eu_risk_class":    self.eu_risk_class.value,
            "compliant":        self.compliant,
            "signature":        self.signature,
            "issued_at":        self.issued_at.isoformat(),
            "expires_at":       self.expires_at.isoformat(),
            "threats_detected": self.threats_detected,
            "framework":        self.metadata.framework,
            "compliance": {
                "eu_ai_act": self.compliance.eu_ai_act,
                "gdpr":      self.compliance.gdpr,
                "hipaa":     self.compliance.hipaa,
                "soc2":      self.compliance.soc2,
            },
        }

    def __repr__(self) -> str:
        return (
            f"<Passport agent='{self.agent_name}' "
            f"did='{self.did}' "
            f"trust={self.trust_score:.2f} "
            f"status={self.status.value}>"
        )
