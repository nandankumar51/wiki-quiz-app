import { useState, useEffect } from 'react'
import { Trash2, Eye, Loader2, RefreshCw } from 'lucide-react'
import { quizAPI } from '../api/quiz'
import QuizDisplay from './QuizDisplay'
import './QuizHistory.css'

function QuizHistory() {
  const [quizzes, setQuizzes] = useState([])
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState(null)
  const [selectedQuiz, setSelectedQuiz] = useState(null)
  const [showModal, setShowModal] = useState(false)

  useEffect(() => {
    fetchQuizzes()
  }, [])

  const fetchQuizzes = async () => {
    setLoading(true)
    setError(null)
    
    try {
      const data = await quizAPI.getAllQuizzes()
      setQuizzes(data)
    } catch (err) {
      setError('Failed to load quiz history')
      console.error('Error:', err)
    } finally {
      setLoading(false)
    }
  }

  const handleViewDetails = async (quizId) => {
    try {
      const data = await quizAPI.getQuizById(quizId)
      setSelectedQuiz(data)
      setShowModal(true)
    } catch (err) {
      console.error('Error fetching quiz details:', err)
      alert('Failed to load quiz details')
    }
  }

  const handleDelete = async (quizId, e) => {
    e.stopPropagation()
    
    if (!confirm('Are you sure you want to delete this quiz?')) {
      return
    }

    try {
      await quizAPI.deleteQuiz(quizId)
      setQuizzes(quizzes.filter(q => q.id !== quizId))
    } catch (err) {
      console.error('Error deleting quiz:', err)
      alert('Failed to delete quiz')
    }
  }

  const formatDate = (dateString) => {
    if (!dateString) return 'N/A'
    const date = new Date(dateString)
    return date.toLocaleDateString('en-US', {
      year: 'numeric',
      month: 'short',
      day: 'numeric',
      hour: '2-digit',
      minute: '2-digit'
    })
  }

  const getArticleName = (url) => {
    try {
      const parts = url.split('/wiki/')
      if (parts.length > 1) {
        return decodeURIComponent(parts[1].replace(/_/g, ' '))
      }
    } catch (e) {
      console.error('Error parsing URL:', e)
    }
    return url
  }

  if (loading) {
    return (
      <div className="loading-container">
        <Loader2 className="spinner" size={40} />
        <p>Loading quiz history...</p>
      </div>
    )
  }

  if (error) {
    return (
      <div className="error-container card">
        <p className="error-text">{error}</p>
        <button className="btn btn-primary" onClick={fetchQuizzes}>
          <RefreshCw size={18} />
          Retry
        </button>
      </div>
    )
  }

  if (quizzes.length === 0) {
    return (
      <div className="empty-state card">
        <h3>No Quizzes Yet</h3>
        <p>Generate your first quiz from the "Generate Quiz" tab!</p>
      </div>
    )
  }

  return (
    <div className="quiz-history">
      <div className="history-header">
        <h2 className="section-title">Quiz History</h2>
        <button className="btn btn-secondary" onClick={fetchQuizzes}>
          <RefreshCw size={18} />
          Refresh
        </button>
      </div>

      <div className="quiz-table-container card">
        <table className="quiz-table">
          <thead>
            <tr>
              <th>Title</th>
              <th>Summary</th>
              <th>Created</th>
              <th>Actions</th>
            </tr>
          </thead>
          <tbody>
            {quizzes.map((quiz) => (
              <tr key={quiz.id}>
                <td>
                  <div className="quiz-title-cell">
                    <strong>{quiz.title}</strong>
                    <a 
                      href={quiz.url} 
                      target="_blank" 
                      rel="noopener noreferrer"
                      className="article-link"
                      onClick={(e) => e.stopPropagation()}
                    >
                      View Article →
                    </a>
                  </div>
                </td>
                <td className="summary-cell">
                  {quiz.summary?.substring(0, 120)}
                  {quiz.summary?.length > 120 && '...'}
                </td>
                <td className="date-cell">{formatDate(quiz.created_at)}</td>
                <td>
                  <div className="action-buttons">
                    <button
                      className="btn-icon btn-primary"
                      onClick={() => handleViewDetails(quiz.id)}
                      title="View Details"
                    >
                      <Eye size={18} />
                    </button>
                    <button
                      className="btn-icon btn-danger"
                      onClick={(e) => handleDelete(quiz.id, e)}
                      title="Delete"
                    >
                      <Trash2 size={18} />
                    </button>
                  </div>
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>

      {/* Modal for viewing quiz details */}
      {showModal && selectedQuiz && (
        <div className="modal-overlay" onClick={() => setShowModal(false)}>
          <div className="modal-content" onClick={(e) => e.stopPropagation()}>
            <div className="modal-header">
              <h2>Quiz Details</h2>
              <button 
                className="modal-close"
                onClick={() => setShowModal(false)}
              >
                ✕
              </button>
            </div>
            <div className="modal-body">
              <QuizDisplay quizData={selectedQuiz} showTakeQuizMode={true} />
            </div>
          </div>
        </div>
      )}
    </div>
  )
}

export default QuizHistory
