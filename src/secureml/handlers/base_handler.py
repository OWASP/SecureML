"""Base handler for all model types"""

from abc import ABC, abstractmethod
from pathlib import Path
from typing import Any, Dict, Optional


class BaseModelHandler(ABC):
    """
    Abstract base class for model handlers

    Each ML framework gets its own handler that knows how to:
    - Save/load models
    - Extract metadata
    - Prepare for signing
    """

    def __init__(self, model: Any):
        """
        Initialize handler

        Args:
            model: Model object
        """
        self.model = model

    @abstractmethod
    def save(self, path: Path) -> Path:
        """
        Save model to disk

        Args:
            path: Output path

        Returns:
            Path to saved model
        """
        pass

    @abstractmethod
    def load(self, path: Path) -> Any:
        """
        Load model from disk

        Args:
            path: Model path

        Returns:
            Loaded model
        """
        pass

    @abstractmethod
    def get_metadata(self) -> Dict[str, Any]:
        """
        Extract model metadata

        Returns:
            Dictionary with model metadata
        """
        pass

    @abstractmethod
    def validate(self) -> bool:
        """
        Validate model integrity

        Returns:
            True if model is valid
        """
        pass

    def get_framework_name(self) -> str:
        """Get framework name"""
        return self.__class__.__name__.replace("Handler", "")
