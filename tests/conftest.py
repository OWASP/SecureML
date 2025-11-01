"""Pytest configuration and fixtures for SecureML tests"""

import pytest
import tempfile
from pathlib import Path
import joblib
import numpy as np
from sklearn.datasets import make_classification
from sklearn.ensemble import RandomForestClassifier


@pytest.fixture
def temp_dir():
    """Create temporary directory for tests"""
    with tempfile.TemporaryDirectory() as tmpdir:
        yield Path(tmpdir)


@pytest.fixture
def sample_data():
    """Generate sample classification data"""
    X, y = make_classification(
        n_samples=100,
        n_features=20,
        n_informative=15,
        n_redundant=5,
        random_state=42
    )
    return X, y


@pytest.fixture
def trained_model(sample_data):
    """Create a trained scikit-learn model"""
    X, y = sample_data
    model = RandomForestClassifier(n_estimators=10, random_state=42)
    model.fit(X, y)
    return model


@pytest.fixture
def saved_model(trained_model, temp_dir):
    """Save model to temporary file"""
    model_path = temp_dir / "model.pkl"
    joblib.dump(trained_model, model_path)
    return model_path


@pytest.fixture
def mock_openssf_available(monkeypatch):
    """Mock OpenSSF model-signing availability"""
    def mock_which(cmd):
        if cmd == "model-signing":
            return "/usr/local/bin/model-signing"
        return None

    import shutil
    monkeypatch.setattr(shutil, "which", mock_which)
