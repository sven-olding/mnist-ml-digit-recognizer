import { useRef, useEffect, useState } from 'react';
import './DrawingCanvas.css';

const DrawingCanvas = () => {
  const canvasRef = useRef(null);
  const [isDrawing, setIsDrawing] = useState(false);
  const [context, setContext] = useState(null);

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
  };

  const getImageData = () => {
    // This will return the canvas data that can be sent to the backend
    // We'll scale it down to 28x28 for MNIST later
    const canvas = canvasRef.current;
    return canvas.toDataURL('image/png');
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
        <button onClick={() => {
          const imageData = getImageData();
          console.log('Image data ready to send:', imageData);
          // TODO: Send to backend for prediction
        }} className="btn btn-predict">
          Predict
        </button>
      </div>
    </div>
  );
};

export default DrawingCanvas;
