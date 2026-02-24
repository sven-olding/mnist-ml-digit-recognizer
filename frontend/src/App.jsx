import './App.css'
import DrawingCanvas from './components/DrawingCanvas'

function App() {
  return (
    <div className="app">
      <header className="app-header">
        <h1>MNIST Digit Recognizer</h1>
        <p>Draw a digit from 0 to 9 and let the AI predict what it is!</p>
      </header>
      <main>
        <DrawingCanvas />
      </main>
    </div>
  )
}

export default App
