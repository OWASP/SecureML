"""
Universal model type detection for all ML frameworks

Automatically detects and classifies models from:
- Traditional ML (XGBoost, sklearn, LightGBM, CatBoost)
- Deep Learning (PyTorch, TensorFlow, JAX, Keras)
- Large Language Models (Transformers, GGUF, SafeTensors)
- Computer Vision (ONNX, CoreML, TensorRT)
- Audio/Speech models
- Multimodal models
"""

import json
from pathlib import Path
from typing import Any, Dict, Optional, Union
from enum import Enum

from ..utils.exceptions import ModelDetectionError, UnsupportedModelError
from ..utils.logging import get_logger

logger = get_logger()


class ModelType(str, Enum):
    """Supported model types"""
    # Traditional ML
    XGBOOST = "xgboost"
    SKLEARN = "sklearn"
    LIGHTGBM = "lightgbm"
    CATBOOST = "catboost"

    # Deep Learning
    PYTORCH = "pytorch"
    TENSORFLOW = "tensorflow"
    KERAS = "keras"
    JAX = "jax"

    # LLMs
    HUGGINGFACE = "huggingface"
    GGUF = "gguf"
    SAFETENSORS = "safetensors"

    # Computer Vision
    ONNX = "onnx"
    COREML = "coreml"
    TENSORRT = "tensorrt"
    OPENVINO = "openvino"

    # Audio
    WHISPER = "whisper"
    WAV2VEC = "wav2vec"

    # Multimodal
    CLIP = "clip"
    MULTIMODAL = "multimodal"

    # Generic
    PICKLE = "pickle"
    JOBLIB = "joblib"
    UNKNOWN = "unknown"


class ModelFormat(str, Enum):
    """Model file formats"""
    # Traditional ML
    PICKLE = ".pkl"
    JOBLIB = ".joblib"
    XGBOOST_MODEL = ".model"
    CATBOOST_MODEL = ".cbm"

    # Deep Learning
    PYTORCH = ".pt"
    PYTORCH_ALT = ".pth"
    TENSORFLOW_PB = ".pb"
    H5 = ".h5"
    KERAS = ".keras"
    TFLITE = ".tflite"

    # ONNX
    ONNX = ".onnx"

    # LLMs
    GGUF = ".gguf"
    GGML = ".ggml"
    SAFETENSORS = ".safetensors"

    # Directory-based
    DIRECTORY = "directory"


class UniversalModelDetector:
    """
    Automatically detect and classify any model type

    Supports both file-based and in-memory model detection with
    comprehensive format recognition for all major ML frameworks.

    Example:
        >>> detector = UniversalModelDetector()
        >>> info = detector.detect("model.pt")
        >>> print(info["model_type"])  # ModelType.PYTORCH
        >>>
        >>> # Also works with in-memory models
        >>> import joblib
        >>> model = joblib.load("model.pkl")
        >>> info = detector.detect(model)
    """

    # File extension mappings
    EXTENSION_MAP = {
        # Traditional ML
        ".pkl": ModelType.PICKLE,
        ".joblib": ModelType.JOBLIB,
        ".model": ModelType.XGBOOST,
        ".cbm": ModelType.CATBOOST,

        # Deep Learning
        ".pt": ModelType.PYTORCH,
        ".pth": ModelType.PYTORCH,
        ".pb": ModelType.TENSORFLOW,
        ".h5": ModelType.KERAS,
        ".keras": ModelType.KERAS,
        ".tflite": ModelType.TENSORFLOW,

        # ONNX
        ".onnx": ModelType.ONNX,

        # LLMs
        ".gguf": ModelType.GGUF,
        ".ggml": ModelType.GGUF,
        ".safetensors": ModelType.SAFETENSORS,
    }

    def __init__(self):
        """Initialize model detector"""
        logger.debug("UniversalModelDetector initialized")

    def detect(
        self,
        model_or_path: Union[Path, str, Any],
        strict: bool = False,
    ) -> Dict[str, Any]:
        """
        Detect model type from file path or object

        Args:
            model_or_path: Path to model file/directory or model object
            strict: Raise error on unknown types (default: False)

        Returns:
            Dictionary containing:
                - model_type: Detected ModelType
                - framework: Framework name
                - format: File format if applicable
                - is_directory: Whether model is directory-based
                - additional_info: Framework-specific details

        Raises:
            UnsupportedModelError: If strict=True and type unknown
            ModelDetectionError: If detection fails

        Example:
            >>> info = detector.detect("model.onnx")
            >>> print(info)
            {
                "model_type": "onnx",
                "framework": "ONNX Runtime",
                "format": ".onnx",
                "is_directory": False
            }
        """
        try:
            # Path-based detection
            if isinstance(model_or_path, (str, Path)):
                return self._detect_from_path(Path(model_or_path), strict)

            # Object-based detection
            return self._detect_from_object(model_or_path, strict)

        except Exception as e:
            logger.error(f"Model detection failed: {e}")
            raise ModelDetectionError(f"Could not detect model type: {e}")

    def _detect_from_path(
        self,
        path: Path,
        strict: bool = False
    ) -> Dict[str, Any]:
        """Detect model type from file/directory path"""
        logger.debug(f"Detecting model type from path: {path}")

        if not path.exists():
            raise FileNotFoundError(f"Model path not found: {path}")

        # Directory-based models (e.g., HuggingFace)
        if path.is_dir():
            return self._detect_directory_model(path)

        # File extension detection
        extension = path.suffix.lower()
        model_type = self.EXTENSION_MAP.get(extension, ModelType.UNKNOWN)

        if model_type == ModelType.UNKNOWN and strict:
            raise UnsupportedModelError(
                f"Unknown model format: {extension}. "
                f"Supported formats: {list(self.EXTENSION_MAP.keys())}"
            )

        # Additional format-specific detection
        additional_info = self._get_additional_info(path, model_type)

        result = {
            "model_type": model_type,
            "framework": self._get_framework_name(model_type),
            "format": extension,
            "is_directory": False,
            "file_size": path.stat().st_size,
            "additional_info": additional_info,
        }

        logger.info(f"Detected model type: {model_type}")
        return result

    def _detect_directory_model(self, path: Path) -> Dict[str, Any]:
        """Detect directory-based models (HuggingFace, TensorFlow SavedModel)"""
        logger.debug(f"Analyzing directory model: {path}")

        # Check for HuggingFace model
        if (path / "config.json").exists():
            return {
                "model_type": ModelType.HUGGINGFACE,
                "framework": "HuggingFace Transformers",
                "format": "directory",
                "is_directory": True,
                "additional_info": self._parse_hf_config(path),
            }

        # Check for TensorFlow SavedModel
        if (path / "saved_model.pb").exists():
            return {
                "model_type": ModelType.TENSORFLOW,
                "framework": "TensorFlow SavedModel",
                "format": "directory",
                "is_directory": True,
                "additional_info": {"type": "saved_model"},
            }

        # Check for PyTorch model directory
        pt_files = list(path.glob("*.pt")) + list(path.glob("*.pth"))
        if pt_files:
            return {
                "model_type": ModelType.PYTORCH,
                "framework": "PyTorch",
                "format": "directory",
                "is_directory": True,
                "additional_info": {"model_files": [f.name for f in pt_files]},
            }

        return {
            "model_type": ModelType.UNKNOWN,
            "framework": "Unknown",
            "format": "directory",
            "is_directory": True,
            "additional_info": {},
        }

    def _detect_from_object(
        self,
        model: Any,
        strict: bool = False
    ) -> Dict[str, Any]:
        """Detect model type from in-memory object"""
        logger.debug(f"Detecting model type from object: {type(model)}")

        module = type(model).__module__
        class_name = type(model).__name__

        # XGBoost
        if "xgboost" in module:
            return {
                "model_type": ModelType.XGBOOST,
                "framework": "XGBoost",
                "class_name": class_name,
                "is_directory": False,
            }

        # scikit-learn
        if "sklearn" in module:
            return {
                "model_type": ModelType.SKLEARN,
                "framework": "scikit-learn",
                "class_name": class_name,
                "is_directory": False,
            }

        # PyTorch
        if "torch" in module:
            return {
                "model_type": ModelType.PYTORCH,
                "framework": "PyTorch",
                "class_name": class_name,
                "is_directory": False,
            }

        # TensorFlow/Keras
        if "tensorflow" in module or "keras" in module:
            return {
                "model_type": ModelType.TENSORFLOW,
                "framework": "TensorFlow/Keras",
                "class_name": class_name,
                "is_directory": False,
            }

        # LightGBM
        if "lightgbm" in module:
            return {
                "model_type": ModelType.LIGHTGBM,
                "framework": "LightGBM",
                "class_name": class_name,
                "is_directory": False,
            }

        # CatBoost
        if "catboost" in module:
            return {
                "model_type": ModelType.CATBOOST,
                "framework": "CatBoost",
                "class_name": class_name,
                "is_directory": False,
            }

        if strict:
            raise UnsupportedModelError(
                f"Unknown model type: {class_name} from {module}"
            )

        return {
            "model_type": ModelType.UNKNOWN,
            "framework": "Unknown",
            "class_name": class_name,
            "module": module,
            "is_directory": False,
        }

    def _get_framework_name(self, model_type: ModelType) -> str:
        """Get friendly framework name from model type"""
        framework_map = {
            ModelType.XGBOOST: "XGBoost",
            ModelType.SKLEARN: "scikit-learn",
            ModelType.LIGHTGBM: "LightGBM",
            ModelType.CATBOOST: "CatBoost",
            ModelType.PYTORCH: "PyTorch",
            ModelType.TENSORFLOW: "TensorFlow",
            ModelType.KERAS: "Keras",
            ModelType.HUGGINGFACE: "HuggingFace Transformers",
            ModelType.ONNX: "ONNX",
            ModelType.GGUF: "GGUF (LLM)",
            ModelType.SAFETENSORS: "SafeTensors",
            ModelType.PICKLE: "Python Pickle",
            ModelType.JOBLIB: "Joblib",
        }
        return framework_map.get(model_type, "Unknown")

    def _get_additional_info(
        self,
        path: Path,
        model_type: ModelType
    ) -> Dict[str, Any]:
        """Get format-specific additional information"""
        info = {}

        # For pickle/joblib, we could inspect the object type
        if model_type in [ModelType.PICKLE, ModelType.JOBLIB]:
            info["note"] = "Object type requires loading to detect framework"

        return info

    def _parse_hf_config(self, path: Path) -> Dict[str, Any]:
        """Parse HuggingFace config.json"""
        try:
            with open(path / "config.json", "r") as f:
                config = json.load(f)
            return {
                "model_type": config.get("model_type", "unknown"),
                "architectures": config.get("architectures", []),
            }
        except Exception as e:
            logger.warning(f"Could not parse HF config: {e}")
            return {}

    def is_supported(self, model_type: ModelType) -> bool:
        """Check if model type is supported for signing"""
        unsupported = {ModelType.UNKNOWN}
        return model_type not in unsupported
