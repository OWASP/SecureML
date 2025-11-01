"""Custom exceptions for SecureML"""


class SecureMLError(Exception):
    """Base exception for all SecureML errors"""
    pass


class SecurityError(SecureMLError):
    """Raised when security verification fails"""
    pass


class ModelDetectionError(SecureMLError):
    """Raised when model type cannot be detected"""
    pass


class SigningError(SecureMLError):
    """Raised when model signing fails"""
    pass


class VerificationError(SecureMLError):
    """Raised when signature verification fails"""
    pass


class OpenSSFNotFoundError(SecureMLError):
    """Raised when OpenSSF model-signing is not installed"""
    pass


class UnsupportedModelError(SecureMLError):
    """Raised when model type is not supported"""
    pass


class KeyManagementError(SecureMLError):
    """Raised when key management operations fail"""
    pass


class ComplianceError(SecureMLError):
    """Raised when compliance validation fails"""
    pass
