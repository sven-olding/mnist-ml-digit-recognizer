#!/usr/bin/env python3
"""
Simple test script to verify the backend setup.
Run this after placing your model file in models/mnist_model.h5
"""

import sys
from pathlib import Path

# Add current directory to path
sys.path.insert(0, str(Path(__file__).parent))


def test_imports():
    """Test if all required packages can be imported."""
    print("Testing imports...")

    try:
        import numpy

        print("✓ numpy")
    except ImportError as e:
        print(f"✗ numpy: {e}")
        return False

    try:
        import PIL

        print("✓ PIL (Pillow)")
    except ImportError as e:
        print(f"✗ PIL: {e}")
        return False

    try:
        import tensorflow

        print(f"✓ tensorflow {tensorflow.__version__}")
    except ImportError as e:
        print(f"✗ tensorflow: {e}")
        return False

    try:
        import fastapi

        print(f"✓ fastapi {fastapi.__version__}")
    except ImportError as e:
        print(f"✗ fastapi: {e}")
        return False

    try:
        import uvicorn

        print("✓ uvicorn")
    except ImportError as e:
        print(f"✗ uvicorn: {e}")
        return False

    return True


def test_model_file():
    """Check if model file exists."""
    print("\nChecking for model file...")

    model_paths = [
        Path("models/mnist_model.h5"),
        Path("models/mnist_model.keras"),
    ]

    for model_path in model_paths:
        if model_path.exists():
            print(f"✓ Found model at {model_path}")
            print(f"  Size: {model_path.stat().st_size / (1024 * 1024):.2f} MB")
            return True

    print("✗ No model file found!")
    print("  Please place your trained model at one of these locations:")
    for path in model_paths:
        print(f"    - {path}")
    return False


def test_model_loading():
    """Try to load the model."""
    print("\nTesting model loading...")

    try:
        from model_loader import model_loader

        model = model_loader.load_model()
        print(f"✓ Model loaded successfully")
        print(f"  Input shape: {model.input_shape}")
        print(f"  Output shape: {model.output_shape}")
        return True
    except FileNotFoundError:
        print("✗ Model file not found")
        return False
    except Exception as e:
        print(f"✗ Error loading model: {e}")
        return False


def main():
    """Run all tests."""
    print("=" * 60)
    print("MNIST Backend Setup Test")
    print("=" * 60)

    imports_ok = test_imports()
    model_exists = test_model_file()

    if imports_ok and model_exists:
        model_loads = test_model_loading()
    else:
        model_loads = False

    print("\n" + "=" * 60)
    print("Test Summary:")
    print(f"  Imports: {'✓ PASS' if imports_ok else '✗ FAIL'}")
    print(f"  Model File: {'✓ PASS' if model_exists else '✗ FAIL'}")
    print(f"  Model Loading: {'✓ PASS' if model_loads else '✗ FAIL'}")
    print("=" * 60)

    if imports_ok and model_exists and model_loads:
        print("\n✓ All tests passed! You can now run the server with:")
        print("  uv run uvicorn main:app --reload")
        print("\nOr if you don't have UV:")
        print("  python -m uvicorn main:app --reload")
        return 0
    else:
        print("\n✗ Some tests failed. Please fix the issues above.")
        if not imports_ok:
            print("\nTo install dependencies:")
            print("  uv sync")
            print("  # or")
            print("  pip install -r pyproject.toml")
        return 1


if __name__ == "__main__":
    sys.exit(main())
