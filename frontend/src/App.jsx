import { useState } from 'react'
import './App.css'
import GenerateQuiz from './components/GenerateQuiz'
import QuizHistory from './components/QuizHistory'

function App() {
  const [activeTab, setActiveTab] = useState('generate')

  return (
    <div className="app">
      <header className="app-header">
        <div className="container">
          <h1 className="app-title">📚 Wiki Quiz Generator</h1>
          <p className="app-subtitle">Generate quizzes from Wikipedia articles using AI</p>
        </div>
      </header>

      <div className="container">
        <div className="tabs">
          <button
            className={`tab ${activeTab === 'generate' ? 'tab-active' : ''}`}
            onClick={() => setActiveTab('generate')}
          >
            Generate Quiz
          </button>
          <button
            className={`tab ${activeTab === 'history' ? 'tab-active' : ''}`}
            onClick={() => setActiveTab('history')}
          >
            Past Quizzes
          </button>
        </div>

        <div className="tab-content">
          {activeTab === 'generate' ? <GenerateQuiz /> : <QuizHistory />}
        </div>
      </div>

      <footer className="app-footer">
        <div className="container">
          <p>Built with FastAPI, React, and Google Gemini AI</p>
        </div>
      </footer>
    </div>
  )
}

export default App
