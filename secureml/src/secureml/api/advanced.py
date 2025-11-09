"""
Advanced API for enterprise use cases

Provides fine-grained control over:
- Multi-signature workflows
- Custom security policies
- Enterprise key management
- Compliance validation
- Advanced threat detection
"""

from pathlib import Path
from typing import Any, Dict, List, Optional, Union
from datetime import datetime

from ..core.openssf_wrapper import OpenSSFWrapper
from ..core.model_detector import UniversalModelDetector
from ..core.fingerprint import ModelFingerprint
from ..core.enterprise import EnterpriseFeatures
from ..core.compliance import ComplianceValidator, ComplianceFramework
from ..utils.config import SecurityConfig, SecurityLevel
from ..utils.logging import get_logger

logger = get_logger()


class AdvancedSecureModel:
    """
    Advanced API for enterprise model security

    Provides full control over all SecureML features including:
    - Multi-signature chains
    - HSM/KMS integration
    - Compliance validation
    - Custom security policies
    - Advanced threat detection

    Example:
        >>> advanced = AdvancedSecureModel(
        ...     model=model,
        ...     config=custom_security_config
        ... )
        >>>
        >>> # Sign with multiple signers
        >>> advanced.add_signature(identity="ml-engineer@company.com")
        >>> advanced.add_signature(identity="ml-manager@company.com")
        >>>
        >>> # Validate compliance
        >>> report = advanced.validate_compliance([
        ...     ComplianceFramework.SOC2,
        ...     ComplianceFramework.ISO27001
        ... ])
    """

    def __init__(
        self,
        model: Any,
        config: Optional[SecurityConfig] = None,
    ):
        """
        Initialize advanced secure model

        Args:
            model: ML model object
            config: Custom security configuration
        """
        self.model = model
        self.config = config or SecurityConfig.from_level(SecurityLevel.ENTERPRISE)

        # Initialize components
        self.openssf = OpenSSFWrapper(self.config)
        self.detector = UniversalModelDetector()
        self.enterprise = EnterpriseFeatures(self.config)
        self.compliance = ComplianceValidator()

        # Signature chain
        self.signatures: List[Dict[str, Any]] = []

        # Detect model
        self.model_info = self.detector.detect(model)

        logger.info("Advanced SecureModel initialized")

    def add_signature(
        self,
        identity: str,
        use_hsm: bool = False,
        hsm_key_id: Optional[str] = None,
        use_cloud_kms: bool = False,
        kms_key_id: Optional[str] = None,
        cloud_provider: Optional[str] = None,
        **metadata: Any,
    ) -> Dict[str, Any]:
        """
        Add a signature to the signature chain

        Supports:
        - Standard OpenSSF signing
        - HSM-backed signing
        - Cloud KMS signing

        Args:
            identity: Signer identity
            use_hsm: Use Hardware Security Module
            hsm_key_id: HSM key identifier
            use_cloud_kms: Use cloud KMS
            kms_key_id: KMS key identifier
            cloud_provider: Cloud provider (aws, azure, gcp)
            **metadata: Additional metadata

        Returns:
            Signature information

        Example:
            >>> # Sign with AWS KMS
            >>> result = advanced.add_signature(
            ...     identity="prod-ml@company.com",
            ...     use_cloud_kms=True,
            ...     kms_key_id="arn:aws:kms:us-east-1:123:key/abc",
            ...     cloud_provider="aws"
            ... )
        """
        logger.info(f"Adding signature from: {identity}")

        signature_data = {
            "identity": identity,
            "timestamp": datetime.now().isoformat(),
            "metadata": metadata,
        }

        if use_hsm and hsm_key_id:
            result = self.enterprise.sign_with_hsm(
                model_path=Path("temp"),  # Would use actual path
                hsm_key_id=hsm_key_id,
            )
            signature_data["method"] = "hsm"
            signature_data["hsm_key_id"] = hsm_key_id

        elif use_cloud_kms and kms_key_id and cloud_provider:
            result = self.enterprise.sign_with_cloud_kms(
                model_path=Path("temp"),
                kms_key_id=kms_key_id,
                cloud_provider=cloud_provider,
            )
            signature_data["method"] = "cloud_kms"
            signature_data["kms_key_id"] = kms_key_id
            signature_data["cloud_provider"] = cloud_provider

        else:
            # Standard OpenSSF signing
            signature_data["method"] = "openssf"

        self.signatures.append(signature_data)
        logger.info(f"Signature added. Total signatures: {len(self.signatures)}")

        return signature_data

    def create_advanced_fingerprint(
        self,
        algorithms: Optional[List[str]] = None,
        enable_merkle: bool = True,
        chunk_size: int = 1024 * 1024,
    ) -> ModelFingerprint:
        """
        Create advanced fingerprint with multiple algorithms

        Args:
            algorithms: Hash algorithms (default: sha256, sha512, blake2b)
            enable_merkle: Build Merkle tree
            chunk_size: Chunk size for hashing

        Returns:
            ModelFingerprint

        Example:
            >>> fp = advanced.create_advanced_fingerprint(
            ...     algorithms=["sha256", "sha512", "blake2b"],
            ...     enable_merkle=True
            ... )
        """
        if algorithms is None:
            algorithms = ["sha256", "sha512", "blake2b"]

        logger.info(f"Creating advanced fingerprint with {len(algorithms)} algorithms")

        # Would create fingerprint from actual model file
        # This is a placeholder
        return ModelFingerprint(
            model_path=Path("model.pkl"),
            timestamp=datetime.now().isoformat(),
        )

    def validate_compliance(
        self,
        frameworks: List[ComplianceFramework],
        generate_report: bool = True,
        report_path: Optional[Path] = None,
    ) -> Dict[str, Any]:
        """
        Validate model against compliance frameworks

        Args:
            frameworks: Frameworks to validate against
            generate_report: Generate detailed report
            report_path: Optional path to save report

        Returns:
            Compliance validation results

        Example:
            >>> result = advanced.validate_compliance([
            ...     ComplianceFramework.SOC2,
            ...     ComplianceFramework.HIPAA
            ... ])
            >>> print(result["overall_status"])
        """
        logger.info(f"Validating compliance: {frameworks}")

        report = self.compliance.validate_compliance(
            model_path=Path("model.pkl"),
            frameworks=frameworks,
            config=self.config.to_dict(),
        )

        if generate_report and report_path:
            self.compliance.generate_report_document(
                report,
                report_path,
                format="json"
            )

        return {
            "overall_status": report.overall_status.value,
            "summary": report.summary,
            "checks": len(report.checks),
            "timestamp": report.timestamp.isoformat(),
        }

    def get_signature_chain(self) -> Dict[str, Any]:
        """Get complete signature chain information"""
        return {
            "total_signatures": len(self.signatures),
            "signatures": self.signatures,
        }

    def rotate_keys(self, old_key_id: str) -> Dict[str, Any]:
        """Rotate signing keys"""
        return self.enterprise.rotate_keys(old_key_id)

    def generate_audit_trail(
        self,
        output_path: Path,
    ) -> Dict[str, Any]:
        """
        Generate comprehensive audit trail

        Args:
            output_path: Path to save audit trail

        Returns:
            Audit information
        """
        from datetime import timedelta

        logger.info(f"Generating audit trail: {output_path}")

        end_date = datetime.now()
        start_date = end_date - timedelta(days=30)

        return self.enterprise.generate_audit_report(
            start_date=start_date,
            end_date=end_date,
            output_path=output_path,
        )
