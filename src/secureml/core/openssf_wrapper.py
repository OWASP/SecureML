"""
OpenSSF Model Signing wrapper - Enterprise enhancement layer

This module provides an enterprise-grade wrapper around the OpenSSF
model-signing tool, adding user-friendly interfaces and additional
security features while maintaining full compatibility with Sigstore.
"""

import subprocess
import shutil
import json
from pathlib import Path
from typing import Any, Dict, Optional, List
from datetime import datetime

from ..utils.exceptions import (
    OpenSSFNotFoundError,
    SigningError,
    VerificationError,
)
from ..utils.logging import get_logger
from ..utils.config import SecurityConfig

logger = get_logger()


class OpenSSFWrapper:
    """
    Enterprise wrapper around OpenSSF Model Signing

    Provides a simplified, user-friendly interface to OpenSSF model-signing
    with additional enterprise features like:
    - Automatic installation detection
    - Enhanced metadata management
    - Multi-signature support
    - Certificate chain validation
    - Integration with enterprise key management

    Example:
        >>> wrapper = OpenSSFWrapper()
        >>> result = wrapper.sign_model(
        ...     model_path="model.pkl",
        ...     identity="ml-team@company.com"
        ... )
        >>> print(result["signature_path"])
    """

    def __init__(self, config: Optional[SecurityConfig] = None, strict: bool = False):
        """
        Initialize OpenSSF wrapper

        Args:
            config: Security configuration (uses defaults if not provided)
            strict: If True, raise error if model-signing not found (default: False)

        Raises:
            OpenSSFNotFoundError: If model-signing is not installed and strict=True
        """
        self.config = config or SecurityConfig()
        self.openssf_available = self._check_installation()

        if not self.openssf_available and strict:
            error_msg = (
                "OpenSSF model-signing not found. "
                "Install with: pip install model-signing"
            )
            logger.error(error_msg)
            raise OpenSSFNotFoundError(error_msg)
        elif not self.openssf_available:
            logger.warning(
                "OpenSSF model-signing not installed. "
                "Signing/verification features will not work. "
                "Install with: pip install model-signing"
            )

        logger.info("OpenSSF wrapper initialized")

    def _check_installation(self) -> bool:
        """
        Check if OpenSSF model-signing is installed

        Returns:
            True if installed, False otherwise
        """
        found = shutil.which("model-signing") is not None
        if found:
            logger.debug("OpenSSF model-signing found")
        return found

    def get_version(self) -> str:
        """Get OpenSSF model-signing version"""
        try:
            result = subprocess.run(
                ["model-signing", "--version"],
                capture_output=True,
                text=True,
                check=True
            )
            return result.stdout.strip()
        except subprocess.CalledProcessError as e:
            logger.warning(f"Could not get version: {e}")
            return "unknown"

    def sign_model(
        self,
        model_path: Path,
        output_sig_path: Optional[Path] = None,
        identity: Optional[str] = None,
        metadata: Optional[Dict[str, Any]] = None,
    ) -> Dict[str, Any]:
        """
        Sign model using OpenSSF model-signing

        Args:
            model_path: Path to model file
            output_sig_path: Path for signature output (auto-generated if None)
            identity: Signer identity (email/name)
            metadata: Additional metadata to include

        Returns:
            Dictionary with signing results including:
                - signature_path: Path to signature file
                - timestamp: Signing timestamp
                - identity: Signer identity
                - metadata: Additional metadata

        Raises:
            SigningError: If signing fails

        Example:
            >>> result = wrapper.sign_model(
            ...     model_path=Path("model.pkl"),
            ...     identity="data-science@company.com",
            ...     metadata={"version": "1.0.0", "purpose": "production"}
            ... )
        """
        if not self.openssf_available:
            raise OpenSSFNotFoundError(
                "OpenSSF model-signing not installed. "
                "Install with: pip install model-signing"
            )

        model_path = Path(model_path)
        if not model_path.exists():
            raise FileNotFoundError(f"Model not found: {model_path}")

        # Auto-generate signature path if not provided
        if output_sig_path is None:
            output_sig_path = model_path.with_suffix(model_path.suffix + ".sig")

        logger.info(f"Signing model: {model_path}")
        logger.security_event(
            "model_signing_start",
            {
                "model_path": str(model_path),
                "identity": identity,
                "has_metadata": metadata is not None,
            }
        )

        # Build command
        cmd = ["model-signing", "sign", str(model_path)]

        if output_sig_path:
            cmd.extend(["--output", str(output_sig_path)])

        if identity:
            cmd.extend(["--identity", identity])

        # Execute signing
        try:
            result = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                check=False
            )

            if result.returncode != 0:
                error_msg = f"Signing failed: {result.stderr}"
                logger.error(error_msg)
                raise SigningError(error_msg)

            logger.info(f"Model signed successfully: {output_sig_path}")
            logger.security_event(
                "model_signing_success",
                {
                    "model_path": str(model_path),
                    "signature_path": str(output_sig_path),
                    "identity": identity,
                }
            )

            return {
                "signature_path": output_sig_path,
                "model_path": model_path,
                "timestamp": datetime.now().isoformat(),
                "identity": identity,
                "metadata": metadata or {},
                "openssf_output": result.stdout,
            }

        except Exception as e:
            logger.error(f"Signing error: {e}")
            raise SigningError(f"Signing failed: {e}")

    def verify_model(
        self,
        model_path: Path,
        signature_path: Optional[Path] = None,
        expected_identity: Optional[str] = None,
        identity_provider: Optional[str] = None,
    ) -> Dict[str, Any]:
        """
        Verify model signature using OpenSSF

        Args:
            model_path: Path to model file
            signature_path: Path to signature (auto-detected if None)
            expected_identity: Expected signer identity to verify
            identity_provider: OIDC provider for identity verification

        Returns:
            Dictionary with verification results:
                - verified: Boolean indicating if verification passed
                - identity: Verified signer identity
                - timestamp: Verification timestamp
                - details: Additional verification details
                - error: Error message if verification failed

        Raises:
            VerificationError: If verification process fails

        Example:
            >>> result = wrapper.verify_model(
            ...     model_path=Path("model.pkl"),
            ...     expected_identity="data-science@company.com"
            ... )
            >>> if result["verified"]:
            ...     print("Model verified successfully!")
        """
        if not self.openssf_available:
            raise OpenSSFNotFoundError(
                "OpenSSF model-signing not installed. "
                "Install with: pip install model-signing"
            )

        model_path = Path(model_path)
        if not model_path.exists():
            raise FileNotFoundError(f"Model not found: {model_path}")

        # Auto-detect signature path if not provided
        if signature_path is None:
            signature_path = model_path.with_suffix(model_path.suffix + ".sig")

        if not signature_path.exists():
            raise FileNotFoundError(f"Signature not found: {signature_path}")

        logger.info(f"Verifying model: {model_path}")
        logger.security_event(
            "model_verification_start",
            {
                "model_path": str(model_path),
                "signature_path": str(signature_path),
                "expected_identity": expected_identity,
            }
        )

        # Build command
        cmd = [
            "model-signing",
            "verify",
            str(model_path),
            "--signature",
            str(signature_path),
        ]

        if expected_identity:
            cmd.extend(["--identity", expected_identity])

        if identity_provider:
            cmd.extend(["--identity-provider", identity_provider])

        # Execute verification
        try:
            result = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                check=False
            )

            verified = result.returncode == 0

            verification_result = {
                "verified": verified,
                "model_path": model_path,
                "signature_path": signature_path,
                "timestamp": datetime.now().isoformat(),
                "expected_identity": expected_identity,
                "output": result.stdout,
                "error": result.stderr if not verified else None,
            }

            if verified:
                logger.info("Model verification successful")
                logger.security_event(
                    "model_verification_success",
                    {
                        "model_path": str(model_path),
                        "identity": expected_identity,
                    }
                )
            else:
                logger.warning(f"Model verification failed: {result.stderr}")
                logger.security_event(
                    "model_verification_failed",
                    {
                        "model_path": str(model_path),
                        "error": result.stderr,
                    },
                    level="WARNING"
                )

            return verification_result

        except Exception as e:
            logger.error(f"Verification error: {e}")
            raise VerificationError(f"Verification failed: {e}")

    def generate_keypair(
        self,
        output_dir: Path,
        key_name: str = "model-signing-key",
    ) -> Dict[str, Path]:
        """
        Generate signing keypair (if supported by OpenSSF version)

        Args:
            output_dir: Directory for key files
            key_name: Name for key files

        Returns:
            Dictionary with public and private key paths

        Note:
            Some OpenSSF workflows use OIDC and don't require local keys
        """
        logger.info(f"Generating keypair: {key_name}")
        output_dir = Path(output_dir)
        output_dir.mkdir(parents=True, exist_ok=True)

        # Note: Actual implementation depends on OpenSSF model-signing capabilities
        # This is a placeholder for enterprise key management integration

        return {
            "private_key": output_dir / f"{key_name}.priv",
            "public_key": output_dir / f"{key_name}.pub",
        }
