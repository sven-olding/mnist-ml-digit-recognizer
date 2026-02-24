#!/bin/bash

# Quick start script for the MNIST backend

echo "================================================"
echo "MNIST Backend - Quick Start"
echo "================================================"
echo ""

# Check if UV is installed
if command -v uv &> /dev/null; then
    echo "✓ UV is installed"
    UV_AVAILABLE=true
else
    echo "✗ UV is not installed"
    echo "  Install UV from: https://github.com/astral-sh/uv"
    echo "  Or use pip instead"
    UV_AVAILABLE=false
fi

echo ""
echo "Step 1: Installing dependencies..."
echo ""

if [ "$UV_AVAILABLE" = true ]; then
    uv sync
else
    # Fallback to pip
    python3 -m pip install fastapi uvicorn tensorflow keras numpy pillow python-multipart
fi

if [ $? -ne 0 ]; then
    echo ""
    echo "✗ Failed to install dependencies"
    exit 1
fi

echo ""
echo "Step 2: Checking model file..."
echo ""

if [ -f "models/mnist_model.h5" ] || [ -f "models/mnist_model.keras" ]; then
    echo "✓ Model file found"
else
    echo "✗ Model file not found!"
    echo ""
    echo "Please place your trained Keras model at:"
    echo "  models/mnist_model.h5"
    echo "  or"
    echo "  models/mnist_model.keras"
    echo ""
    echo "You can still run the setup test with:"
    echo "  python test_setup.py"
    exit 1
fi

echo ""
echo "Step 3: Running setup test..."
echo ""

if [ "$UV_AVAILABLE" = true ]; then
    uv run python test_setup.py
else
    python3 test_setup.py
fi

if [ $? -eq 0 ]; then
    echo ""
    echo "================================================"
    echo "✓ Setup complete!"
    echo "================================================"
    echo ""
    echo "To start the server, run:"
    if [ "$UV_AVAILABLE" = true ]; then
        echo "  uv run uvicorn main:app --reload --host 0.0.0.0 --port 8000"
    else
        echo "  python3 -m uvicorn main:app --reload --host 0.0.0.0 --port 8000"
    fi
    echo ""
    echo "The API will be available at:"
    echo "  http://localhost:8000"
    echo "  Docs: http://localhost:8000/docs"
else
    echo ""
    echo "✗ Setup failed. Please check the errors above."
    exit 1
fi
