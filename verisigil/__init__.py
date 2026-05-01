"""
VeriSigil AI — Trust Infrastructure for Autonomous AI Agents
============================================================
"""

from .client import VeriSigil
from .passport import Passport, PassportStatus
from .exceptions import (
    VeriSigilError,
    AuthenticationError,
    PassportNotFoundError,
    ComplianceError,
    RateLimitError,
)
from .version import __version__

__all__ = [
    "VeriSigil",
    "Passport",
    "PassportStatus",
    "VeriSigilError",
    "AuthenticationError",
    "PassportNotFoundError",
    "ComplianceError",
    "RateLimitError",
    "__version__",
]
