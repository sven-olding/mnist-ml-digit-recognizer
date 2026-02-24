# MNIST Digit Recognition App

A full-stack web application for handwritten digit recognition using machine learning. Draw a digit on the canvas, and the trained neural network will predict what digit you drew.

## Overview

This project consists of:
- **Frontend**: React application with an interactive drawing canvas
- **Backend**: FastAPI service serving a TensorFlow/Keras MNIST model
- **ML Model**: Neural network trained on the MNIST dataset

## Project Structure

```
mnist-ml/
├── backend/          # Python FastAPI backend
│   ├── main.py       # API server
│   ├── train_model.py # Model training script
│   ├── models/       # Trained models
│   └── ...
└── frontend/         # React frontend
    ├── src/
    │   ├── components/
    │   └── App.jsx
    └── ...
```

## Quick Start

### Backend Setup

```bash
cd backend

# Install dependencies
uv sync

# Train the model (optional - model already included)
uv run python train_model.py

# Start the API server
uv run uvicorn main:app --reload
```

Backend will run at `http://localhost:8000`

See [backend/README.md](backend/README.md) for detailed backend documentation.

### Frontend Setup

```bash
cd frontend

# Install dependencies
npm install

# Start the development server
npm run dev
```

Frontend will run at `http://localhost:5173`

See [frontend/README.md](frontend/README.md) for detailed frontend documentation.

## Features

- ✏️ **Interactive Drawing Canvas**: Draw digits with your mouse
- 🧠 **Real-time Predictions**: Get instant digit recognition from the ML model
- 📊 **Confidence Scores**: See prediction probabilities for all digits (0-9)
- 🎨 **Clean, Modern UI**: Responsive design optimized for digit drawing
- 🚀 **Fast API**: High-performance FastAPI backend with TensorFlow

## Tech Stack

### Frontend
- React 19
- Vite
- HTML5 Canvas API
- CSS3

### Backend
- Python 3.11+
- FastAPI
- TensorFlow/Keras
- Uvicorn
- UV package manager

### Machine Learning
- TensorFlow Datasets (MNIST)
- Keras Sequential Model
- Simple feedforward neural network architecture

## Model Training

The model is trained on the MNIST dataset with:
- **Input**: 28x28 grayscale images
- **Architecture**: Flatten → Dense(128, ReLU) → Dense(10)
- **Optimizer**: Adam (lr=0.001)
- **Epochs**: 6
- **Accuracy**: ~98% on test set

To retrain the model:
```bash
cd backend
uv run python train_model.py
```

## API Endpoints

- `GET /` - Health check
- `POST /predict` - Predict digit from image
- `GET /health` - Service health with model status
- `GET /docs` - Interactive API documentation (Swagger UI)

## Development

### Prerequisites
- Python 3.11+
- Node.js 16+
- UV package manager ([install](https://github.com/astral-sh/uv))
- npm

### Running Both Services

Terminal 1 (Backend):
```bash
cd backend
uv run uvicorn main:app --reload
```

Terminal 2 (Frontend):
```bash
cd frontend
npm run dev
```

## License

MIT

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.
