# MNIST Digit Recognizer - Frontend

A React-based web application for drawing digits and using ML to recognize them.

## Features

- **Interactive Drawing Canvas**: Draw digits (0-9) on a 280x280 pixel canvas
- **Clean UI**: Modern, responsive design optimized for digit drawing
- **MNIST Ready**: Canvas optimized for digit recognition (can be scaled to 28x28 for MNIST model)
- **Clear & Predict Controls**: Easy-to-use buttons for clearing the canvas and triggering predictions

## Getting Started

### Prerequisites
- Node.js (v16 or higher)
- npm

### Installation

```bash
cd frontend
npm install
```

### Running the Development Server

```bash
npm run dev
```

The app will be available at `http://localhost:5173/`

### Building for Production

```bash
npm run build
```

## Project Structure

```
frontend/
├── src/
│   ├── components/
│   │   ├── DrawingCanvas.jsx    # Main canvas component with drawing logic
│   │   └── DrawingCanvas.css    # Canvas-specific styles
│   ├── App.jsx                  # Main application component
│   ├── App.css                  # App-level styles
│   ├── index.css                # Global styles
│   └── main.jsx                 # Application entry point
├── index.html
├── package.json
└── vite.config.js
```

## Drawing Canvas Component

The `DrawingCanvas` component provides:
- Mouse-based drawing with smooth lines
- Configurable line width (optimized at 15px for digit recognition)
- White background with black strokes (matches MNIST training data)
- Canvas dimensions: 280x280 display (can be scaled to 28x28 for ML model)
- Export functionality via `getImageData()` method

## Next Steps

- [ ] Implement touch support for mobile devices
- [ ] Add preprocessing to scale canvas to 28x28 pixels
- [ ] Add prediction history

## Technologies Used

- **React 19** - UI framework
- **Vite** - Build tool and dev server
- **HTML5 Canvas API** - Drawing functionality
- **CSS3** - Styling

## Canvas Drawing Details

The canvas uses the HTML5 Canvas API with the following configuration:
- Line width: 15px (provides good digit clarity)
- Line cap: round (smooth stroke endpoints)
- Line join: round (smooth corners)
- Background: white
- Stroke color: black

This configuration matches the MNIST dataset format (white background, dark digits).

