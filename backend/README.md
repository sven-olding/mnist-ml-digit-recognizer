# MNIST Backend API

Python backend API for serving MNIST digit recognition predictions using a trained Keras model.

## Tech Stack

- **Python 3.11+**
- **UV** - Modern Python package manager
- **FastAPI** - High-performance web framework
- **TensorFlow/Keras** - ML model inference
- **Uvicorn** - ASGI server

## Setup

### Prerequisites
- Python 3.11 or higher
- UV package manager ([install here](https://github.com/astral-sh/uv))

### Installation

```bash
cd backend

# Install dependencies using UV
uv sync

# Or if you prefer using pip
uv pip install -e .
```

### Model File

The trained model is located in `models/mnist_model.keras`. 

To train a new model, see the **Training the Model** section below.

Supported formats: `.h5`, `.keras`

## Running the Server

### Development Mode

```bash
# Using UV
uv run uvicorn main:app --reload --host 0.0.0.0 --port 8000

# Or activate the virtual environment and run
uv run python -m uvicorn main:app --reload
```

### Production Mode

```bash
uv run uvicorn main:app --host 0.0.0.0 --port 8000 --workers 4
```

The API will be available at `http://localhost:8000`

## Training the Model

To train or retrain the MNIST model:

```bash
# Activate the environment
source .venv/bin/activate

# Or use UV directly
uv run python train_model.py
```

This will:
1. Download the MNIST dataset (via TensorFlow Datasets)
2. Train a neural network for 6 epochs
3. Save the trained model to `models/mnist_model.keras`

The training script uses:
- **Dataset**: MNIST from TensorFlow Datasets
- **Architecture**: Simple feedforward neural network
  - Flatten layer (28x28 -> 784)
  - Dense layer (128 units, ReLU)
  - Dense layer (10 units, output)
- **Optimizer**: Adam (learning rate: 0.001)
- **Loss**: Sparse Categorical Crossentropy
- **Batch size**: 128
- **Epochs**: 6

Training typically takes a few minutes on CPU, faster with GPU support.

## API Endpoints

### `GET /`
Health check endpoint
```json
{
  "status": "ok",
  "message": "MNIST Digit Recognition API"
}
```

### `POST /predict`
Predict digit from image

**Request:**
- Content-Type: `multipart/form-data`
- Body: `image` - Image file (PNG/JPEG) or base64 encoded string

**Response:**
```json
{
  "prediction": 7,
  "confidence": 0.9856,
  "probabilities": [0.001, 0.002, 0.003, ..., 0.9856, ...]
}
```

### `GET /health`
Service health check with model status

## API Documentation

Once the server is running, visit:
- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

## Project Structure

```
backend/
├── main.py              # FastAPI application and routes
├── model_loader.py      # Model loading and caching
├── image_processor.py   # Image preprocessing
├── pyproject.toml       # UV/pip dependencies
├── models/              # Directory for model files
│   └── mnist_model.keras
└── README.md
```

## Image Preprocessing

Images are automatically processed to match MNIST requirements:
1. Converted to grayscale
2. Resized to 28x28 pixels
3. Normalized to [0, 1] range
4. Inverted if needed (white background → black background)
5. Reshaped to (1, 28, 28, 1) for model input

## Testing

```bash
# Run tests
uv run pytest

# Test the API with curl
curl -X POST "http://localhost:8000/predict" \
  -F "image=@test_digit.png"
```

## Environment Variables

- `MODEL_PATH` - Path to the Keras model file (default: `models/mnist_model.keras`)
- `PORT` - Server port (default: 8000)
- `HOST` - Server host (default: 0.0.0.0)

## CORS Configuration

CORS is enabled for development with the frontend running on `http://localhost:5173`
