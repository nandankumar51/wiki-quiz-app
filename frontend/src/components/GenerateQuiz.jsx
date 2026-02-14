import { useState } from 'react'
import { Loader2, ExternalLink, AlertCircle } from 'lucide-react'
import { quizAPI } from '../api/quiz'
import QuizDisplay from './QuizDisplay'
import './GenerateQuiz.css'

function GenerateQuiz() {
  const [url, setUrl] = useState('')
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState(null)
  const [quizData, setQuizData] = useState(null)
  const [showPreview, setShowPreview] = useState(false)

  const validateWikipediaUrl = (url) => {
    const pattern = /^https?:\/\/(en\.)?wikipedia\.org\/wiki\/.+/
    return pattern.test(url)
  }

  const handleGenerate = async () => {
    setError(null)
    setQuizData(null)

    // Validate URL
    if (!url.trim()) {
      setError('Please enter a Wikipedia URL')
      return
    }

    if (!validateWikipediaUrl(url)) {
      setError('Please enter a valid Wikipedia article URL (e.g., https://en.wikipedia.org/wiki/Article_Name)')
      return
    }

    setLoading(true)

    try {
      const data = await quizAPI.generateQuiz(url)
      setQuizData(data)
      setShowPreview(false)
    } catch (err) {
      setError(err.response?.data?.detail || 'Failed to generate quiz. Please try again.')
      console.error('Error:', err)
    } finally {
      setLoading(false)
    }
  }

  const handleUrlChange = (e) => {
    setUrl(e.target.value)
    setError(null)
  }

  const handleKeyPress = (e) => {
    if (e.key === 'Enter' && !loading) {
      handleGenerate()
    }
  }

  // Sample URLs for quick testing
  const sampleUrls = [
    'https://en.wikipedia.org/wiki/Alan_Turing',
    'https://en.wikipedia.org/wiki/Artificial_intelligence',
    'https://en.wikipedia.org/wiki/Albert_Einstein',
  ]

  return (
    <div className="generate-quiz">
      <div className="input-section card">
        <h2 className="section-title">Generate Quiz from Wikipedia Article</h2>
        
        <div className="url-input-group">
          <input
            type="text"
            className="input url-input"
            placeholder="Enter Wikipedia URL (e.g., https://en.wikipedia.org/wiki/Alan_Turing)"
            value={url}
            onChange={handleUrlChange}
            onKeyPress={handleKeyPress}
            disabled={loading}
          />
          <button
            className="btn btn-primary generate-btn"
            onClick={handleGenerate}
            disabled={loading}
          >
            {loading ? (
              <>
                <Loader2 className="spinner" size={18} />
                Generating...
              </>
            ) : (
              'Generate Quiz'
            )}
          </button>
        </div>

        {error && (
          <div className="error-message">
            <AlertCircle size={18} />
            <span>{error}</span>
          </div>
        )}

        <div className="sample-urls">
          <p className="sample-label">Try these examples:</p>
          <div className="sample-buttons">
            {sampleUrls.map((sampleUrl, index) => (
              <button
                key={index}
                className="btn-link"
                onClick={() => setUrl(sampleUrl)}
                disabled={loading}
              >
                {sampleUrl.split('/wiki/')[1].replace(/_/g, ' ')}
              </button>
            ))}
          </div>
        </div>
      </div>

      {quizData && (
        <div className="quiz-result">
          <QuizDisplay quizData={quizData} showTakeQuizMode={true} />
        </div>
      )}
    </div>
  )
}

export default GenerateQuiz
