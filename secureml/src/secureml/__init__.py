"""
SecureML - Enterprise-Ready AI Model Security Platform
Built on OpenSSF Model Signing Standard

SecureML is the "Stripe for model security" - making enterprise-grade
AI model protection accessible, user-friendly, and production-ready.

Features:
- Universal model support (XGBoost, PyTorch, TensorFlow, LLMs, etc.)
- Built on OpenSSF Model Signing v1.0
- Enterprise security features (HSM, KMS, compliance)
- Advanced threat detection and forensics
- Simple, elegant API for developers
"""

__version__ = "0.1.2"
__author__ = "SecureML Team"
__license__ = "Apache-2.0"

from .core.openssf_wrapper import OpenSSFWrapper
from .core.model_detector import UniversalModelDetector
from .core.watermark import (
    ModelWatermark,
    WatermarkConfig,
    WatermarkType,
    WatermarkMethod,
    TriggerSet,
)
from .api.simple import SecureModel

__all__ = [
    "SecureModel",
    "OpenSSFWrapper",
    "UniversalModelDetector",
    "ModelWatermark",
    "WatermarkConfig",
    "WatermarkType",
    "WatermarkMethod",
    "TriggerSet",
    "__version__",
]
