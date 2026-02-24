"""
Image preprocessing utilities for MNIST digit recognition.
Converts input images to the format expected by the MNIST model (28x28 grayscale).
"""

import io
import base64
import numpy as np
from PIL import Image


def preprocess_image(image_data: bytes) -> np.ndarray:
    """
    Preprocess image data for MNIST model prediction.

    Args:
        image_data: Raw image bytes (PNG, JPEG, etc.)

    Returns:
        Preprocessed numpy array of shape (1, 28, 28, 1)
    """
    # Open image and convert to grayscale
    image = Image.open(io.BytesIO(image_data))
    image = image.convert("L")  # Convert to grayscale

    # Resize to 28x28 (MNIST standard)
    image = image.resize((28, 28), Image.Resampling.LANCZOS)

    # Convert to numpy array
    img_array = np.array(image)

    # Invert if needed (MNIST expects white digits on black background)
    # If the background is white (high values), invert it
    if np.mean(img_array) > 127:
        img_array = 255 - img_array

    # Normalize to [0, 1]
    img_array = img_array.astype("float32") / 255.0

    # Reshape to (1, 28, 28, 1) for model input
    img_array = img_array.reshape(1, 28, 28, 1)

    return img_array


def preprocess_base64_image(base64_string: str) -> np.ndarray:
    """
    Preprocess base64 encoded image for MNIST model prediction.

    Args:
        base64_string: Base64 encoded image string (with or without data URI prefix)

    Returns:
        Preprocessed numpy array of shape (1, 28, 28, 1)
    """
    # Remove data URI prefix if present
    if "," in base64_string:
        base64_string = base64_string.split(",")[1]

    # Decode base64 to bytes
    image_data = base64.b64decode(base64_string)

    return preprocess_image(image_data)


def visualize_preprocessed_image(img_array: np.ndarray) -> str:
    """
    Convert preprocessed image array back to base64 for debugging.

    Args:
        img_array: Preprocessed numpy array of shape (1, 28, 28, 1)

    Returns:
        Base64 encoded PNG string
    """
    # Remove batch and channel dimensions
    img = (img_array[0, :, :, 0] * 255).astype(np.uint8)

    # Convert to PIL Image
    pil_img = Image.fromarray(img, mode="L")

    # Convert to base64
    buffer = io.BytesIO()
    pil_img.save(buffer, format="PNG")
    img_str = base64.b64encode(buffer.getvalue()).decode()

    return f"data:image/png;base64,{img_str}"
