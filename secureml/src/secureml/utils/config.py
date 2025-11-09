"""Configuration management for SecureML"""

from enum import Enum
from pathlib import Path
from typing import Any, Dict, List, Optional
from dataclasses import dataclass, field
import yaml


class SecurityLevel(str, Enum):
    """Security levels for model protection"""
    BASIC = "basic"
    STANDARD = "standard"
    ENTERPRISE = "enterprise"
    MAXIMUM = "maximum"


class ComplianceFramework(str, Enum):
    """Supported compliance frameworks"""
    SOC2 = "soc2"
    ISO27001 = "iso27001"
    FIPS_140_2 = "fips_140_2"
    HIPAA = "hipaa"
    GDPR = "gdpr"


@dataclass
class SecurityConfig:
    """Security configuration for SecureML"""

    # Core settings
    security_level: SecurityLevel = SecurityLevel.STANDARD
    enable_openssf: bool = True

    # Advanced features
    enable_fingerprinting: bool = False
    enable_merkle_trees: bool = False
    enable_audit_logging: bool = False
    enable_encryption: bool = False

    # Hash algorithms
    hash_algorithms: List[str] = field(default_factory=lambda: ["sha256"])

    # Compliance
    compliance_frameworks: List[ComplianceFramework] = field(default_factory=list)

    # Key management
    use_hsm: bool = False
    kms_provider: Optional[str] = None  # "aws", "azure", "gcp"
    key_rotation_days: int = 90

    # Threat detection
    enable_threat_detection: bool = False
    enable_forensics: bool = False

    @classmethod
    def from_level(cls, level: SecurityLevel) -> "SecurityConfig":
        """Create config from security level preset"""
        configs = {
            SecurityLevel.BASIC: cls(
                security_level=SecurityLevel.BASIC,
                enable_fingerprinting=False,
                enable_merkle_trees=False,
                enable_audit_logging=False,
            ),
            SecurityLevel.STANDARD: cls(
                security_level=SecurityLevel.STANDARD,
                enable_fingerprinting=True,
                enable_audit_logging=True,
                hash_algorithms=["sha256", "sha512"],
            ),
            SecurityLevel.ENTERPRISE: cls(
                security_level=SecurityLevel.ENTERPRISE,
                enable_fingerprinting=True,
                enable_merkle_trees=True,
                enable_audit_logging=True,
                enable_threat_detection=True,
                hash_algorithms=["sha256", "sha512", "blake2b"],
            ),
            SecurityLevel.MAXIMUM: cls(
                security_level=SecurityLevel.MAXIMUM,
                enable_fingerprinting=True,
                enable_merkle_trees=True,
                enable_audit_logging=True,
                enable_encryption=True,
                enable_threat_detection=True,
                enable_forensics=True,
                hash_algorithms=["sha256", "sha512", "blake2b"],
            ),
        }
        return configs[level]

    @classmethod
    def from_yaml(cls, path: Path) -> "SecurityConfig":
        """Load config from YAML file"""
        with open(path, "r") as f:
            data = yaml.safe_load(f)
        return cls(**data)

    def to_yaml(self, path: Path) -> None:
        """Save config to YAML file"""
        data = {
            "security_level": self.security_level.value,
            "enable_openssf": self.enable_openssf,
            "enable_fingerprinting": self.enable_fingerprinting,
            "enable_merkle_trees": self.enable_merkle_trees,
            "enable_audit_logging": self.enable_audit_logging,
            "enable_encryption": self.enable_encryption,
            "hash_algorithms": self.hash_algorithms,
            "compliance_frameworks": [f.value for f in self.compliance_frameworks],
            "use_hsm": self.use_hsm,
            "kms_provider": self.kms_provider,
            "key_rotation_days": self.key_rotation_days,
            "enable_threat_detection": self.enable_threat_detection,
            "enable_forensics": self.enable_forensics,
        }
        with open(path, "w") as f:
            yaml.dump(data, f, default_flow_style=False)

    def to_dict(self) -> Dict[str, Any]:
        """Convert config to dictionary"""
        return {
            "security_level": self.security_level.value,
            "enable_openssf": self.enable_openssf,
            "enable_fingerprinting": self.enable_fingerprinting,
            "enable_merkle_trees": self.enable_merkle_trees,
            "enable_audit_logging": self.enable_audit_logging,
            "enable_encryption": self.enable_encryption,
            "hash_algorithms": self.hash_algorithms,
            "compliance_frameworks": [f.value for f in self.compliance_frameworks],
            "use_hsm": self.use_hsm,
            "kms_provider": self.kms_provider,
            "key_rotation_days": self.key_rotation_days,
            "enable_threat_detection": self.enable_threat_detection,
            "enable_forensics": self.enable_forensics,
        }
