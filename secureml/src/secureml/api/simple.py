"""
Simple, user-friendly API for SecureML

This is the main interface most users will interact with.
Provides a Pythonic, intuitive API similar to popular ML libraries.

Example:
    >>> from secureml import SecureModel
    >>> import joblib
    >>>
    >>> # Load and secure your model in one line
    >>> model = joblib.load("model.pkl")
    >>> secure_model = SecureModel(model)
    >>> secure_model.sign(identity="ml-team@company.com")
    >>> secure_model.save("model_signed.sml")
    >>>
    >>> # Load and verify
    >>> verified_model = SecureModel.load("model_signed.sml", verify=True)
    >>> predictions = verified_model.predict(X_test)
"""

import joblib
import json
import shutil
import tempfile
from pathlib import Path
from typing import Any, Dict, Optional, Union
from datetime import datetime

from ..core.openssf_wrapper import OpenSSFWrapper
from ..core.model_detector import UniversalModelDetector, ModelType
from ..core.fingerprint import ModelFingerprint
from ..core.watermark import ModelWatermark, WatermarkConfig, WatermarkType, TriggerSet
from ..utils.config import SecurityConfig, SecurityLevel
from ..utils.logging import get_logger
from ..utils.exceptions import SecurityError, SigningError, VerificationError
from .. import __version__

logger = get_logger()


class SecureModel:
    """
    Main user-facing class for securing ML models

    Simple, elegant interface for model security that works with
    any ML framework. Built on OpenSSF Model Signing with enterprise
    enhancements.

    The "Stripe for model security" - simple yet powerful.

    Example:
        >>> # Secure any model in 3 lines
        >>> model = joblib.load("model.pkl")
        >>> secure_model = SecureModel(model)
        >>> secure_model.sign_and_save("model.sml", creator="team@company.com")
        >>>
        >>> # Load and verify
        >>> model = SecureModel.load("model.sml", verify=True)
        >>> predictions = model.predict(X_test)
    """

    def __init__(
        self,
        model: Optional[Any] = None,
        security_level: Union[SecurityLevel, str] = SecurityLevel.STANDARD,
        config: Optional[SecurityConfig] = None,
    ):
        """
        Initialize SecureModel

        Args:
            model: ML model object (any framework)
            security_level: Security level preset
            config: Custom security configuration

        Example:
            >>> model = xgb.XGBClassifier()
            >>> secure_model = SecureModel(model, security_level="enterprise")
        """
        self.model = model
        self._model_path: Optional[Path] = None
        self._signature_path: Optional[Path] = None
        self._metadata: Dict[str, Any] = {}
        self._watermark: Optional[ModelWatermark] = None

        # Security configuration
        if isinstance(security_level, str):
            security_level = SecurityLevel(security_level)
        self.security_level = security_level
        self.config = config or SecurityConfig.from_level(security_level)

        # Initialize components
        self.openssf = OpenSSFWrapper(self.config)
        self.detector = UniversalModelDetector()

        # Detect model type if provided
        if model is not None:
            self._detect_model_info()

        logger.info(f"SecureModel initialized with {security_level} security")

    def _detect_model_info(self) -> None:
        """Detect and store model information"""
        try:
            self._model_info = self.detector.detect(self.model)
            logger.debug(f"Detected model type: {self._model_info.get('model_type')}")
        except Exception as e:
            logger.warning(f"Could not detect model type: {e}")
            self._model_info = {}

    def sign(
        self,
        identity: str,
        output_path: Optional[Union[str, Path]] = None,
        **metadata: Any,
    ) -> Dict[str, Any]:
        """
        Sign the model using OpenSSF

        Args:
            identity: Signer identity (email)
            output_path: Optional custom output path for signature
            **metadata: Additional metadata (version, description, etc.)

        Returns:
            Signing result with paths and metadata

        Example:
            >>> result = secure_model.sign(
            ...     identity="data-science@company.com",
            ...     version="2.0.0",
            ...     description="Production fraud detection model"
            ... )
        """
        if self.model is None:
            raise ValueError("No model loaded. Load a model first.")

        logger.info(f"Signing model with identity: {identity}")

        # Save model to temporary file for signing
        temp_dir = Path(tempfile.mkdtemp())
        model_path = temp_dir / "model.pkl"

        try:
            # Save model
            joblib.dump(self.model, model_path, compress=3)

            # Sign with OpenSSF
            sig_path = Path(output_path) if output_path else model_path.with_suffix(".pkl.sig")
            sign_result = self.openssf.sign_model(
                model_path=model_path,
                output_sig_path=sig_path,
                identity=identity,
                metadata=metadata,
            )

            # Store paths
            self._model_path = model_path
            self._signature_path = sig_path

            # Store metadata
            self._metadata = {
                "creator": identity,
                "created_at": datetime.now().isoformat(),
                "security_level": self.security_level.value,
                "secureml_version": __version__,
                "model_info": getattr(self, '_model_info', {}),
                **metadata,
            }

            logger.info("Model signed successfully")
            return sign_result

        except Exception as e:
            logger.error(f"Signing failed: {e}")
            raise SigningError(f"Failed to sign model: {e}")

    def save(
        self,
        output_path: Union[str, Path],
        include_fingerprint: bool = None,
    ) -> Dict[str, str]:
        """
        Save signed model as SecureML package

        Creates a .sml package containing:
        - Model file
        - OpenSSF signature
        - Metadata
        - Optional fingerprint

        Args:
            output_path: Path for .sml package
            include_fingerprint: Include advanced fingerprint (default: based on security level)

        Returns:
            Dictionary with package information

        Example:
            >>> secure_model.save("model_v2.sml")
        """
        if self._signature_path is None:
            raise ValueError("Model not signed. Call sign() first.")

        output_path = Path(output_path).with_suffix('.sml')
        logger.info(f"Saving SecureML package: {output_path}")

        # Determine if fingerprint should be included
        if include_fingerprint is None:
            include_fingerprint = self.config.enable_fingerprinting

        # Create package directory
        output_path.mkdir(parents=True, exist_ok=True)

        # Copy model and signature
        shutil.copy(self._model_path, output_path / "model.pkl")
        shutil.copy(self._signature_path, output_path / "model.pkl.sig")

        # Create fingerprint if enabled
        if include_fingerprint:
            fingerprint = ModelFingerprint.create(
                model_path=self._model_path,
                algorithms=self.config.hash_algorithms,
                enable_merkle=self.config.enable_merkle_trees,
            )
            fingerprint.to_json(output_path / "fingerprint.json")

        # Save watermark data if present
        if self._watermark:
            self._watermark.save_watermark(output_path / "watermark.json")
            logger.info("Watermark data saved to package")

        # Save metadata
        with open(output_path / "metadata.json", "w") as f:
            json.dump(self._metadata, f, indent=2)

        # Create manifest
        manifest = {
            "format_version": "1.0",
            "created_with": f"secureml {__version__}",
            "components": ["model.pkl", "model.pkl.sig", "metadata.json"],
            "security_level": self.security_level.value,
            "has_watermark": self._watermark is not None,
        }
        if include_fingerprint:
            manifest["components"].append("fingerprint.json")
        if self._watermark:
            manifest["components"].append("watermark.json")

        with open(output_path / "manifest.json", "w") as f:
            json.dump(manifest, f, indent=2)

        logger.info(f"SecureML package saved: {output_path}")

        return {
            "package_path": str(output_path),
            "model_path": str(output_path / "model.pkl"),
            "signature_path": str(output_path / "model.pkl.sig"),
            "metadata_path": str(output_path / "metadata.json"),
        }

    def sign_and_save(
        self,
        output_path: Union[str, Path],
        identity: str,
        **metadata: Any,
    ) -> Dict[str, str]:
        """
        Sign and save in one convenient call

        Args:
            output_path: Path for .sml package
            identity: Signer identity
            **metadata: Additional metadata

        Returns:
            Package information

        Example:
            >>> secure_model.sign_and_save(
            ...     "model.sml",
            ...     identity="ml-team@company.com",
            ...     version="1.0.0"
            ... )
        """
        self.sign(identity=identity, **metadata)
        return self.save(output_path)

    @classmethod
    def load(
        cls,
        package_path: Union[str, Path],
        verify: bool = True,
        verify_fingerprint: bool = None,
    ) -> "SecureModel":
        """
        Load and optionally verify a SecureML package

        Args:
            package_path: Path to .sml package
            verify: Verify OpenSSF signature (default: True)
            verify_fingerprint: Verify fingerprint if available

        Returns:
            SecureModel instance with loaded model

        Raises:
            SecurityError: If verification fails
            FileNotFoundError: If package not found

        Example:
            >>> model = SecureModel.load("model.sml", verify=True)
            >>> if model.is_verified:
            ...     predictions = model.predict(X_test)
        """
        package_path = Path(package_path)
        logger.info(f"Loading SecureML package: {package_path}")

        if not package_path.exists():
            raise FileNotFoundError(f"Package not found: {package_path}")

        # Load metadata
        with open(package_path / "metadata.json", "r") as f:
            metadata = json.load(f)

        # Load manifest
        with open(package_path / "manifest.json", "r") as f:
            manifest = json.load(f)

        # Verify signature if requested
        verified = False
        if verify:
            logger.info("Verifying model signature...")
            openssf = OpenSSFWrapper()
            verify_result = openssf.verify_model(
                model_path=package_path / "model.pkl",
                signature_path=package_path / "model.pkl.sig",
                expected_identity=metadata.get("creator"),
            )

            if not verify_result["verified"]:
                raise SecurityError(
                    f"Signature verification failed: {verify_result.get('error')}"
                )

            verified = True
            logger.info("Signature verification passed")

        # Verify fingerprint if available and requested
        if verify_fingerprint or (verify_fingerprint is None and (package_path / "fingerprint.json").exists()):
            if (package_path / "fingerprint.json").exists():
                logger.info("Verifying model fingerprint...")
                fingerprint = ModelFingerprint.from_json(package_path / "fingerprint.json")
                if not fingerprint.verify():
                    raise SecurityError("Fingerprint verification failed - model may be tampered")
                logger.info("Fingerprint verification passed")

        # Load model
        model = joblib.load(package_path / "model.pkl")

        # Create SecureModel instance
        security_level = SecurityLevel(metadata.get("security_level", "standard"))
        secure_model = cls(model=model, security_level=security_level)
        secure_model._metadata = metadata
        secure_model._verified = verified

        # Load watermark data if present
        watermark_path = package_path / "watermark.json"
        if watermark_path.exists():
            logger.info("Loading watermark data...")
            secure_model._watermark = ModelWatermark.load_watermark(watermark_path)
            logger.info("Watermark data loaded successfully")

        logger.info("SecureML package loaded successfully")
        return secure_model

    def predict(self, *args: Any, **kwargs: Any) -> Any:
        """
        Make predictions using the model

        Args:
            *args: Arguments passed to model.predict()
            **kwargs: Keyword arguments passed to model.predict()

        Returns:
            Model predictions

        Example:
            >>> predictions = secure_model.predict(X_test)
        """
        if self.model is None:
            raise ValueError("No model loaded")

        if not hasattr(self.model, "predict"):
            raise AttributeError(
                f"Model of type {type(self.model).__name__} "
                "does not have a predict method"
            )

        return self.model.predict(*args, **kwargs)

    def predict_proba(self, *args: Any, **kwargs: Any) -> Any:
        """Get prediction probabilities (if supported)"""
        if self.model is None:
            raise ValueError("No model loaded")

        if not hasattr(self.model, "predict_proba"):
            raise AttributeError(
                f"Model of type {type(self.model).__name__} "
                "does not support predict_proba"
            )

        return self.model.predict_proba(*args, **kwargs)

    @property
    def is_verified(self) -> bool:
        """Check if model has been verified"""
        return getattr(self, '_verified', False)

    @property
    def metadata(self) -> Dict[str, Any]:
        """Get model metadata"""
        return self._metadata

    def get_info(self) -> Dict[str, Any]:
        """Get complete model information"""
        info = {
            "security_level": self.security_level.value,
            "verified": self.is_verified,
            "model_info": getattr(self, '_model_info', {}),
            "metadata": self._metadata,
            "config": self.config.to_dict(),
        }

        # Add watermark info if present
        if self._watermark:
            info["watermark"] = self._watermark.get_info()

        return info

    def embed_watermark(
        self,
        owner: str,
        watermark_type: Union[WatermarkType, str] = WatermarkType.PARAMETER,
        strength: float = 0.01,
        trigger_set: Optional[TriggerSet] = None,
        **kwargs: Any,
    ) -> Dict[str, Any]:
        """
        Embed watermark into the model for IP protection

        This embeds an invisible watermark that can be used to prove
        ownership of the model. The watermark is designed to be robust
        against model modifications like fine-tuning or compression.

        Args:
            owner: Owner identifier (email, organization, etc.)
            watermark_type: Type of watermarking (parameter, trigger_set, statistical)
            strength: Watermark strength (0.001-0.1, default 0.01)
            trigger_set: Optional trigger set for backdoor watermarking
            **kwargs: Additional watermark configuration options

        Returns:
            Dictionary with watermark embedding result

        Example:
            >>> # Parameter watermarking (white-box)
            >>> result = secure_model.embed_watermark(
            ...     owner="ml-team@company.com",
            ...     watermark_type=WatermarkType.PARAMETER,
            ...     strength=0.01
            ... )
            >>> print(f"Watermark ID: {result['watermark_id']}")
            >>>
            >>> # Trigger set watermarking (black-box)
            >>> trigger_set = TriggerSet(
            ...     inputs=np.array([[1, 2, 3], [4, 5, 6]]),
            ...     outputs=np.array([0, 1])
            ... )
            >>> result = secure_model.embed_watermark(
            ...     owner="ml-team@company.com",
            ...     watermark_type=WatermarkType.TRIGGER_SET,
            ...     trigger_set=trigger_set
            ... )
        """
        if self.model is None:
            raise ValueError("No model loaded. Load a model first.")

        logger.info(f"Embedding watermark for owner: {owner}")

        # Convert string to enum if needed
        if isinstance(watermark_type, str):
            watermark_type = WatermarkType(watermark_type)

        # Create watermark config
        config = WatermarkConfig(
            watermark_type=watermark_type,
            strength=strength,
            **kwargs
        )

        # Initialize watermark
        self._watermark = ModelWatermark(
            owner=owner,
            config=config,
        )

        # Embed watermark
        result = self._watermark.embed(self.model, trigger_set=trigger_set)

        # Store in metadata
        self._metadata["watermark"] = {
            "watermark_id": self._watermark.watermark_id,
            "owner": owner,
            "type": watermark_type.value,
            "embedded_at": datetime.now().isoformat(),
        }

        logger.info(f"Watermark embedded: {self._watermark.watermark_id}")

        return {
            "success": result.success,
            "watermark_id": result.watermark_id,
            "owner": owner,
            "type": watermark_type.value,
            "message": result.message,
            "timestamp": result.timestamp,
        }

    def verify_watermark(
        self,
        trigger_set: Optional[TriggerSet] = None,
    ) -> Dict[str, Any]:
        """
        Verify embedded watermark in the model

        Args:
            trigger_set: Optional trigger set for verification

        Returns:
            Dictionary with verification result and score

        Raises:
            ValueError: If no watermark has been embedded

        Example:
            >>> # Verify watermark
            >>> result = secure_model.verify_watermark()
            >>> if result['verified']:
            ...     print(f"Watermark verified! Score: {result['score']:.3f}")
            ...     print(f"Owner: {result['owner']}")
            >>> else:
            ...     print("Watermark verification failed")
        """
        if self._watermark is None:
            raise ValueError(
                "No watermark available for verification. "
                "Either embed a watermark or load a watermarked model."
            )

        logger.info("Verifying watermark...")

        result = self._watermark.verify(self.model, trigger_set=trigger_set)

        logger.info(
            f"Watermark verification: {'PASSED' if result.success else 'FAILED'} "
            f"(score: {result.verification_score:.3f})"
        )

        return {
            "verified": result.success,
            "watermark_id": result.watermark_id,
            "owner": self._watermark.owner,
            "score": result.verification_score,
            "message": result.message,
            "timestamp": result.timestamp,
        }

    @property
    def has_watermark(self) -> bool:
        """Check if model has an embedded watermark"""
        return self._watermark is not None

    @property
    def watermark_info(self) -> Optional[Dict[str, Any]]:
        """Get watermark information"""
        if self._watermark:
            return self._watermark.get_info()
        return None
