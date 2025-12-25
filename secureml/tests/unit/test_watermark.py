"""Tests for ModelWatermark functionality"""

import pytest
import numpy as np
from sklearn.ensemble import RandomForestClassifier
from sklearn.datasets import make_classification

from secureml.core.watermark import (
    ModelWatermark,
    WatermarkConfig,
    WatermarkType,
    WatermarkMethod,
    TriggerSet,
    WatermarkResult,
)


@pytest.fixture
def sample_model():
    """Create a simple sklearn model for testing"""
    X, y = make_classification(n_samples=100, n_features=10, random_state=42)
    model = RandomForestClassifier(n_estimators=5, max_depth=3, random_state=42)
    model.fit(X, y)
    return model


@pytest.fixture
def watermark_instance():
    """Create a watermark instance"""
    return ModelWatermark(
        owner="test@example.com",
        config=WatermarkConfig(
            watermark_type=WatermarkType.PARAMETER,
            method=WatermarkMethod.LSB,
            strength=0.01,
            embed_rate=0.1,
        )
    )


class TestModelWatermark:
    """Test ModelWatermark class"""

    def test_watermark_initialization(self):
        """Test watermark can be initialized"""
        watermark = ModelWatermark(owner="test@example.com")
        assert watermark is not None
        assert watermark.owner == "test@example.com"
        assert watermark.watermark_id is not None

    def test_watermark_id_generation(self):
        """Test watermark ID is unique"""
        wm1 = ModelWatermark(owner="test1@example.com")
        wm2 = ModelWatermark(owner="test2@example.com")
        assert wm1.watermark_id != wm2.watermark_id

    def test_secret_key_generation(self):
        """Test secret key is generated"""
        watermark = ModelWatermark(owner="test@example.com")
        assert watermark.secret_key is not None
        assert len(watermark.secret_key) > 0

    def test_custom_watermark_id(self):
        """Test custom watermark ID"""
        custom_id = "custom123"
        watermark = ModelWatermark(owner="test@example.com", watermark_id=custom_id)
        assert watermark.watermark_id == custom_id


class TestParameterWatermarking:
    """Test parameter watermarking"""

    def test_embed_parameter_watermark(self, sample_model, watermark_instance):
        """Test embedding parameter watermark"""
        result = watermark_instance.embed(sample_model)

        assert isinstance(result, WatermarkResult)
        assert result.success is True
        assert result.watermark_id == watermark_instance.watermark_id
        assert "params_modified" in result.metadata

    def test_verify_parameter_watermark(self, sample_model, watermark_instance):
        """Test verifying parameter watermark"""
        # Embed watermark
        embed_result = watermark_instance.embed(sample_model)
        assert embed_result.success is True

        # Verify watermark
        verify_result = watermark_instance.verify(sample_model)

        assert isinstance(verify_result, WatermarkResult)
        assert verify_result.verification_score is not None
        assert 0.0 <= verify_result.verification_score <= 1.0

    def test_watermark_different_strengths(self, sample_model):
        """Test watermarking with different strengths"""
        strengths = [0.001, 0.01, 0.1]

        for strength in strengths:
            watermark = ModelWatermark(
                owner="test@example.com",
                config=WatermarkConfig(strength=strength)
            )
            result = watermark.embed(sample_model)
            assert result.success is True

    def test_watermark_different_embed_rates(self, sample_model):
        """Test watermarking with different embed rates"""
        embed_rates = [0.05, 0.1, 0.2]

        for rate in embed_rates:
            watermark = ModelWatermark(
                owner="test@example.com",
                config=WatermarkConfig(embed_rate=rate)
            )
            result = watermark.embed(sample_model)
            assert result.success is True


class TestTriggerSetWatermarking:
    """Test trigger set watermarking"""

    def test_trigger_set_creation(self):
        """Test trigger set creation"""
        inputs = np.random.rand(10, 5)
        outputs = np.random.randint(0, 2, 10)

        trigger_set = TriggerSet(
            inputs=inputs,
            outputs=outputs,
            description="Test trigger set"
        )

        assert trigger_set.verify_size() is True
        assert len(trigger_set.inputs) == len(trigger_set.outputs)

    def test_trigger_set_invalid_size(self):
        """Test trigger set with mismatched sizes"""
        inputs = np.random.rand(10, 5)
        outputs = np.random.randint(0, 2, 5)  # Different size

        trigger_set = TriggerSet(inputs=inputs, outputs=outputs)
        assert trigger_set.verify_size() is False

    def test_embed_trigger_watermark(self, sample_model):
        """Test embedding trigger set watermark"""
        watermark = ModelWatermark(
            owner="test@example.com",
            config=WatermarkConfig(watermark_type=WatermarkType.TRIGGER_SET)
        )

        trigger_set = TriggerSet(
            inputs=np.random.rand(5, 10),
            outputs=np.array([0, 1, 0, 1, 0]),
            description="Test triggers"
        )

        result = watermark.embed(sample_model, trigger_set=trigger_set)
        assert result.success is True


class TestStatisticalWatermarking:
    """Test statistical watermarking"""

    def test_embed_statistical_watermark(self, sample_model):
        """Test embedding statistical watermark"""
        watermark = ModelWatermark(
            owner="test@example.com",
            config=WatermarkConfig(watermark_type=WatermarkType.STATISTICAL)
        )

        result = watermark.embed(sample_model)
        assert result.success is True
        assert result.method == "statistical"

    def test_verify_statistical_watermark(self, sample_model):
        """Test verifying statistical watermark"""
        watermark = ModelWatermark(
            owner="test@example.com",
            config=WatermarkConfig(watermark_type=WatermarkType.STATISTICAL)
        )

        # Embed
        embed_result = watermark.embed(sample_model)
        assert embed_result.success is True

        # Verify
        verify_result = watermark.verify(sample_model)
        assert verify_result.verification_score is not None


class TestWatermarkPersistence:
    """Test watermark save/load functionality"""

    def test_save_watermark(self, watermark_instance, sample_model, tmp_path):
        """Test saving watermark data"""
        # Embed watermark
        watermark_instance.embed(sample_model)

        # Save
        save_path = tmp_path / "watermark_data.json"
        watermark_instance.save_watermark(save_path)

        assert save_path.exists()

    def test_load_watermark(self, watermark_instance, sample_model, tmp_path):
        """Test loading watermark data"""
        # Embed and save
        watermark_instance.embed(sample_model)
        save_path = tmp_path / "watermark_data.json"
        watermark_instance.save_watermark(save_path)

        # Load
        loaded_watermark = ModelWatermark.load_watermark(save_path)

        assert loaded_watermark.watermark_id == watermark_instance.watermark_id
        assert loaded_watermark.owner == watermark_instance.owner

    def test_verify_after_load(self, watermark_instance, sample_model, tmp_path):
        """Test verification after loading watermark"""
        # Embed and save
        watermark_instance.embed(sample_model)
        save_path = tmp_path / "watermark_data.json"
        watermark_instance.save_watermark(save_path)

        # Load and verify
        loaded_watermark = ModelWatermark.load_watermark(save_path)
        result = loaded_watermark.verify(sample_model)

        assert result.verification_score is not None


class TestWatermarkInfo:
    """Test watermark information retrieval"""

    def test_get_info(self, watermark_instance):
        """Test getting watermark information"""
        info = watermark_instance.get_info()

        assert "watermark_id" in info
        assert "owner" in info
        assert "type" in info
        assert "method" in info
        assert info["owner"] == "test@example.com"

    def test_info_after_embedding(self, watermark_instance, sample_model):
        """Test info after embedding"""
        watermark_instance.embed(sample_model)
        info = watermark_instance.get_info()

        assert info["has_watermark_data"] is True


class TestWatermarkConfig:
    """Test watermark configuration"""

    def test_config_defaults(self):
        """Test default configuration"""
        config = WatermarkConfig()

        assert config.watermark_type == WatermarkType.PARAMETER
        assert config.method == WatermarkMethod.LSB
        assert config.strength > 0
        assert config.embed_rate > 0
        assert config.verify_threshold > 0

    def test_config_custom_values(self):
        """Test custom configuration values"""
        config = WatermarkConfig(
            watermark_type=WatermarkType.TRIGGER_SET,
            method=WatermarkMethod.BACKDOOR,
            strength=0.05,
            embed_rate=0.2,
            verify_threshold=0.9
        )

        assert config.watermark_type == WatermarkType.TRIGGER_SET
        assert config.method == WatermarkMethod.BACKDOOR
        assert config.strength == 0.05
        assert config.embed_rate == 0.2
        assert config.verify_threshold == 0.9


class TestParameterExtraction:
    """Test parameter extraction from models"""

    def test_extract_sklearn_parameters(self, sample_model, watermark_instance):
        """Test extracting parameters from sklearn model"""
        params = watermark_instance._extract_parameters(sample_model)

        assert isinstance(params, dict)
        assert len(params) > 0

    def test_extract_parameters_returns_dict(self, sample_model, watermark_instance):
        """Test parameter extraction returns dict"""
        params = watermark_instance._extract_parameters(sample_model)

        assert isinstance(params, dict)
        for key, value in params.items():
            assert isinstance(value, np.ndarray)
