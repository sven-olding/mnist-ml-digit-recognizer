"""
Model loader utility for loading and caching the Keras MNIST model.
"""

import os
from pathlib import Path
from typing import Optional
import tensorflow as tf
from tensorflow import keras


class ModelLoader:
    """Singleton class for loading and caching the Keras model."""

    _instance: Optional["ModelLoader"] = None
    _model: Optional[keras.Model] = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def load_model(self, model_path: Optional[str] = None) -> keras.Model:
        """
        Load the Keras model from disk. Caches the model after first load.

        Args:
            model_path: Path to the model file. If None, uses default path.

        Returns:
            Loaded Keras model

        Raises:
            FileNotFoundError: If model file doesn't exist
        """
        if self._model is not None:
            return self._model

        # Determine model path
        if model_path is None:
            model_path = os.getenv("MODEL_PATH", "models/mnist_model.keras")

        model_file = Path(model_path)

        # Check if model exists
        if not model_file.exists():
            raise FileNotFoundError(
                f"Model file not found at {model_file.absolute()}. "
                f"Please place your trained Keras model at this location."
            )

        print(f"Loading model from {model_file.absolute()}...")

        # Load the model
        self._model = keras.models.load_model(str(model_file))

        print(f"Model loaded successfully!")
        print(f"Model input shape: {self._model.input_shape}")
        print(f"Model output shape: {self._model.output_shape}")

        return self._model

    def get_model(self) -> Optional[keras.Model]:
        """Get the cached model without loading."""
        return self._model

    def is_loaded(self) -> bool:
        """Check if model is loaded."""
        return self._model is not None


# Global instance
model_loader = ModelLoader()
