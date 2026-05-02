"""
VeriSigil AI — Custom Exceptions
==================================
"""


class VeriSigilError(Exception):
    """Base exception for all VeriSigil errors."""
    pass


class AuthenticationError(VeriSigilError):
    """Raised when API key is invalid or missing."""
    pass


class PassportNotFoundError(VeriSigilError):
    """Raised when no passport exists for the requested agent ID."""
    pass


class ComplianceError(VeriSigilError):
    """Raised when an agent fails a compliance check."""
    pass


class RateLimitError(VeriSigilError):
    """Raised when the API rate limit is exceeded."""
    pass


class SecurityThreatError(VeriSigilError):
    """Raised when a security scan detects critical threats."""
    pass


class PassportExpiredError(VeriSigilError):
    """Raised when an operation is attempted with an expired passport."""
    pass


class RevocationError(VeriSigilError):
    """Raised when a passport revocation fails."""
    pass
