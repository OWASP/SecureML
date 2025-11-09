"""Tests for UniversalModelDetector"""

import pytest
from pathlib import Path
from secureml.core.model_detector import UniversalModelDetector, ModelType


class TestModelDetector:
    """Test model detection functionality"""

    def test_detector_initialization(self):
        """Test detector can be initialized"""
        detector = UniversalModelDetector()
        assert detector is not None

    def test_detect_pickle_extension(self, saved_model):
        """Test detection of .pkl files"""
        detector = UniversalModelDetector()
        result = detector.detect(saved_model)

        assert result["model_type"] == ModelType.PICKLE
        assert result["format"] == ".pkl"
        assert not result["is_directory"]

    def test_detect_sklearn_object(self, trained_model):
        """Test detection of sklearn model object"""
        detector = UniversalModelDetector()
        result = detector.detect(trained_model)

        assert result["model_type"] == ModelType.SKLEARN
        assert result["framework"] == "scikit-learn"
        assert "RandomForest" in result["class_name"]

    def test_strict_mode_unknown_type(self, temp_dir):
        """Test strict mode raises error for unknown types"""
        detector = UniversalModelDetector()

        # Create file with unknown extension
        unknown_file = temp_dir / "model.xyz"
        unknown_file.touch()

        with pytest.raises(Exception):
            detector.detect(unknown_file, strict=True)

    def test_extension_mapping(self):
        """Test extension map contains common formats"""
        detector = UniversalModelDetector()

        assert ".pkl" in detector.EXTENSION_MAP
        assert ".pt" in detector.EXTENSION_MAP
        assert ".h5" in detector.EXTENSION_MAP
        assert ".onnx" in detector.EXTENSION_MAP
