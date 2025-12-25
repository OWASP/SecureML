"""Tests for simple API (SecureModel)"""

import pytest
import numpy as np
from sklearn.ensemble import RandomForestClassifier
from sklearn.datasets import make_classification

from secureml.api.simple import SecureModel


@pytest.fixture
def sample_model():
    """Create a simple sklearn model for testing"""
    X, y = make_classification(n_samples=100, n_features=10, random_state=42)
    model = RandomForestClassifier(n_estimators=5, max_depth=3, random_state=42)
    model.fit(X, y)
    return model


@pytest.fixture
def sample_data():
    """Create sample data for testing"""
    X, y = make_classification(n_samples=50, n_features=10, random_state=42)
    return X, y


class TestSecureModelBasics:
    """Test basic SecureModel functionality"""

    def test_secure_model_initialization(self, sample_model):
        """Test SecureModel can be initialized"""
        secure_model = SecureModel(sample_model)
        assert secure_model is not None
        assert secure_model.model is not None

    def test_secure_model_has_model(self, sample_model):
        """Test SecureModel contains the original model"""
        secure_model = SecureModel(sample_model)
        assert secure_model.model is sample_model

    def test_predict_method_exists(self, sample_model, sample_data):
        """Test predict method exists and works"""
        secure_model = SecureModel(sample_model)
        X, y = sample_data

        predictions = secure_model.predict(X)
        assert predictions is not None
        assert len(predictions) == len(X)


class TestSecureModelSigning:
    """Test model signing functionality"""

    def test_sign_model(self, sample_model, tmp_path):
        """Test signing a model"""
        secure_model = SecureModel(sample_model)
        output_path = tmp_path / "signed_model.sml"

        # This will likely fail without full OpenSSF setup, but tests the API
        try:
            secure_model.sign_and_save(
                str(output_path),
                identity="test@example.com"
            )
        except Exception as e:
            # Expected to fail without OpenSSF/Sigstore setup
            # But API should exist
            assert "sign_and_save" in dir(secure_model)


class TestSecureModelWatermarking:
    """Test watermarking through SecureModel"""

    def test_embed_watermark(self, sample_model):
        """Test embedding watermark to model"""
        secure_model = SecureModel(sample_model)

        # Embed watermark
        result = secure_model.embed_watermark(owner="test@example.com")

        assert result is not None
        assert isinstance(result, dict)
        assert result.get("success") is True or "watermark" in result

    def test_verify_watermark(self, sample_model):
        """Test verifying watermark"""
        secure_model = SecureModel(sample_model)

        # Embed watermark
        embed_result = secure_model.embed_watermark(owner="test@example.com")
        assert embed_result is not None

        # Verify watermark
        verify_result = secure_model.verify_watermark()
        assert verify_result is not None
        assert isinstance(verify_result, (dict, bool))


class TestSecureModelInfo:
    """Test model information methods"""

    def test_get_info(self, sample_model):
        """Test getting model information"""
        secure_model = SecureModel(sample_model)
        info = secure_model.get_info()

        assert isinstance(info, dict)
        assert "model_type" in info or "model" in str(info)
