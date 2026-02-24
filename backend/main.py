"""
FastAPI backend for MNIST digit recognition.
Serves predictions from a trained Keras model.
"""

import os
from typing import Union
from contextlib import asynccontextmanager

import numpy as np
from fastapi import FastAPI, File, UploadFile, HTTPException, Form
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from model_loader import model_loader
from image_processor import preprocess_image, preprocess_base64_image


# Lifespan context manager for startup/shutdown events
@asynccontextmanager
async def lifespan(app: FastAPI):
    """Load the model on startup and cleanup on shutdown."""
    # Startup: Load the model
    try:
        model_loader.load_model()
        print("✓ Model loaded successfully")
    except FileNotFoundError as e:
        print(f"✗ Error loading model: {e}")
        print("The API will start but predictions will fail until a model is provided.")

    yield

    # Shutdown: Cleanup if needed
    print("Shutting down...")


# Create FastAPI app
app = FastAPI(
    title="MNIST Digit Recognition API",
    description="API for predicting handwritten digits using a trained Keras model",
    version="1.0.0",
    lifespan=lifespan,
)

# Configure CORS for frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",  # Vite dev server
        "http://127.0.0.1:5173",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Response models
class PredictionResponse(BaseModel):
    """Response model for prediction endpoint."""

    prediction: int
    confidence: float
    probabilities: list[float]


class HealthResponse(BaseModel):
    """Response model for health check."""

    status: str
    model_loaded: bool
    message: str


@app.get("/", tags=["Health"])
async def root():
    """Root endpoint - basic health check."""
    return {"status": "ok", "message": "MNIST Digit Recognition API", "docs": "/docs"}


@app.get("/health", response_model=HealthResponse, tags=["Health"])
async def health_check():
    """Detailed health check including model status."""
    model_loaded = model_loader.is_loaded()

    return HealthResponse(
        status="healthy" if model_loaded else "degraded",
        model_loaded=model_loaded,
        message="Model loaded and ready" if model_loaded else "Model not loaded",
    )


@app.post("/predict", response_model=PredictionResponse, tags=["Prediction"])
async def predict_digit(
    image: Union[UploadFile, None] = File(None), image_data: Union[str, None] = Form(None)
):
    """
    Predict the digit from an uploaded image or base64 encoded image data.

    Args:
        image: Image file (PNG, JPEG, etc.)
        image_data: Base64 encoded image string (alternative to file upload)

    Returns:
        PredictionResponse with predicted digit, confidence, and all probabilities
    """
    # Check if model is loaded
    model = model_loader.get_model()
    if model is None:
        raise HTTPException(
            status_code=503, detail="Model not loaded. Please ensure the model file exists."
        )

    # Get preprocessed image
    try:
        if image is not None:
            # Process uploaded file
            contents = await image.read()
            img_array = preprocess_image(contents)
        elif image_data is not None:
            # Process base64 string
            img_array = preprocess_base64_image(image_data)
        else:
            raise HTTPException(
                status_code=400,
                detail="Either 'image' file or 'image_data' string must be provided",
            )
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Error processing image: {str(e)}")

    # Make prediction
    try:
        predictions = model.predict(img_array, verbose=0)
        probabilities = predictions[0].tolist()

        # Get the predicted digit (highest probability)
        predicted_digit = int(np.argmax(predictions[0]))
        confidence = float(probabilities[predicted_digit])

        return PredictionResponse(
            prediction=predicted_digit, confidence=confidence, probabilities=probabilities
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error during prediction: {str(e)}")


@app.get("/model-info", tags=["Info"])
async def model_info():
    """Get information about the loaded model."""
    model = model_loader.get_model()

    if model is None:
        raise HTTPException(status_code=503, detail="Model not loaded")

    return {
        "input_shape": str(model.input_shape),
        "output_shape": str(model.output_shape),
        "model_type": type(model).__name__,
    }


if __name__ == "__main__":
    import uvicorn

    port = int(os.getenv("PORT", 8000))
    host = os.getenv("HOST", "0.0.0.0")

    uvicorn.run("main:app", host=host, port=port, reload=True)
