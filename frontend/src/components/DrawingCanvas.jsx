import { useRef, useEffect, useState } from 'react';
import './DrawingCanvas.css';

const DrawingCanvas = () => {
  const canvasRef = useRef(null);
  const [isDrawing, setIsDrawing] = useState(false);
  const [context, setContext] = useState(null);
  const [prediction, setPrediction] = useState(null);
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState(null);

  // Canvas dimensions - larger display size for better UX
  const displayWidth = 280;
  const displayHeight = 280;
  
  useEffect(() => {
    const canvas = canvasRef.current;
    if (canvas) {
      const ctx = canvas.getContext('2d');
      ctx.fillStyle = 'white';
      ctx.fillRect(0, 0, displayWidth, displayHeight);
      ctx.strokeStyle = 'black';
      ctx.lineWidth = 15;
      ctx.lineCap = 'round';
      ctx.lineJoin = 'round';
      setContext(ctx);
    }
  }, []);

  const startDrawing = (e) => {
    if (!context) return;
    
    const rect = canvasRef.current.getBoundingClientRect();
    const x = e.clientX - rect.left;
    const y = e.clientY - rect.top;
    
    context.beginPath();
    context.moveTo(x, y);
    setIsDrawing(true);
  };

  const draw = (e) => {
    if (!isDrawing || !context) return;
    
    const rect = canvasRef.current.getBoundingClientRect();
    const x = e.clientX - rect.left;
    const y = e.clientY - rect.top;
    
    context.lineTo(x, y);
    context.stroke();
  };

  const stopDrawing = () => {
    if (context) {
      context.closePath();
    }
    setIsDrawing(false);
  };

  const clearCanvas = () => {
    if (context) {
      context.fillStyle = 'white';
      context.fillRect(0, 0, displayWidth, displayHeight);
    }
    setPrediction(null);
    setError(null);
  };

  const getImageData = () => {
    // This will return the canvas data that can be sent to the backend
    // We'll scale it down to 28x28 for MNIST later
    const canvas = canvasRef.current;
    return canvas.toDataURL('image/png');
  };

  const handlePredict = async () => {
    setIsLoading(true);
    setError(null);
    
    try {
      const imageData = getImageData();
      
      // Remove the data:image/png;base64, prefix
      const base64Data = imageData.split(',')[1];
      
      // Create form data to send to the backend
      const formData = new FormData();
      formData.append('image_data', imageData);
      
      // Call the backend API
      const response = await fetch('http://localhost:8000/predict', {
        method: 'POST',
        body: formData,
      });
      
      if (!response.ok) {
        throw new Error(`Prediction failed: ${response.statusText}`);
      }
      
      const result = await response.json();
      setPrediction(result);
    } catch (err) {
      console.error('Prediction error:', err);
      setError(err.message || 'Failed to get prediction');
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="drawing-canvas-container">
      <h2>Draw a Digit (0-9)</h2>
      <canvas
        ref={canvasRef}
        width={displayWidth}
        height={displayHeight}
        onMouseDown={startDrawing}
        onMouseMove={draw}
        onMouseUp={stopDrawing}
        onMouseLeave={stopDrawing}
        className="drawing-canvas"
      />
      <div className="canvas-controls">
        <button onClick={clearCanvas} className="btn btn-clear">
          Clear
        </button>
        <button 
          onClick={handlePredict} 
          className="btn btn-predict"
          disabled={isLoading}
        >
          {isLoading ? 'Predicting...' : 'Predict'}
        </button>
      </div>
      
      {error && (
        <div className="prediction-result error">
          <p>Error: {error}</p>
        </div>
      )}
      
      {prediction && (
        <div className="prediction-result">
          <h3>Prediction: <span className="predicted-digit">{prediction.prediction}</span></h3>
          <p className="confidence">Confidence: {(prediction.confidence * 100).toFixed(2)}%</p>
          <div className="probabilities">
            <h4>All Probabilities:</h4>
            <div className="probability-bars">
              {prediction.probabilities.map((prob, index) => (
                <div key={index} className="probability-item">
                  <span className="digit-label">{index}</span>
                  <div className="probability-bar-container">
                    <div 
                      className="probability-bar"
                      style={{ width: `${prob * 100}%` }}
                    />
                  </div>
                  <span className="probability-value">{(prob * 100).toFixed(1)}%</span>
                </div>
              ))}
            </div>
          </div>
        </div>
      )}
    </div>
  );
};

export default DrawingCanvas;
