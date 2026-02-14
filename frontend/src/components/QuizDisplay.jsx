import { useState } from 'react'
import { ExternalLink, CheckCircle, XCircle, Award } from 'lucide-react'
import './QuizDisplay.css'

function QuizDisplay({ quizData, showTakeQuizMode = false }) {
  const [quizMode, setQuizMode] = useState(false)
  const [userAnswers, setUserAnswers] = useState({})
  const [submitted, setSubmitted] = useState(false)

  if (!quizData) return null

  const handleAnswerSelect = (questionIndex, answer) => {
    if (submitted) return
    setUserAnswers({
      ...userAnswers,
      [questionIndex]: answer
    })
  }

  const handleSubmit = () => {
    if (Object.keys(userAnswers).length === 0) {
      alert('Please answer at least one question!')
      return
    }
    setSubmitted(true)
  }

  const handleReset = () => {
    setUserAnswers({})
    setSubmitted(false)
  }

  const calculateScore = () => {
    let correct = 0
    quizData.quiz.forEach((question, index) => {
      if (userAnswers[index] === question.answer) {
        correct++
      }
    })
    return {
      correct,
      total: quizData.quiz.length,
      percentage: Math.round((correct / quizData.quiz.length) * 100)
    }
  }

  const score = submitted ? calculateScore() : null

  const getDifficultyColor = (difficulty) => {
    switch (difficulty?.toLowerCase()) {
      case 'easy': return 'badge-easy'
      case 'medium': return 'badge-medium'
      case 'hard': return 'badge-hard'
      default: return 'badge-medium'
    }
  }

  return (
    <div className="quiz-display">
      {/* Article Info */}
      <div className="article-info card">
        <div className="article-header">
          <div>
            <h2 className="article-title">{quizData.title}</h2>
            <a 
              href={quizData.url} 
              target="_blank" 
              rel="noopener noreferrer"
              className="article-link"
            >
              View Wikipedia Article <ExternalLink size={16} />
            </a>
          </div>
          
          {showTakeQuizMode && (
            <button
              className={`btn ${quizMode ? 'btn-secondary' : 'btn-primary'}`}
              onClick={() => {
                setQuizMode(!quizMode)
                setUserAnswers({})
                setSubmitted(false)
              }}
            >
              {quizMode ? 'View Answers' : 'Take Quiz'}
            </button>
          )}
        </div>

        <p className="article-summary">{quizData.summary}</p>

        {/* Key Entities */}
        {quizData.key_entities && (
          <div className="entities-section">
            <h3 className="subsection-title">Key Entities</h3>
            <div className="entities-grid">
              {quizData.key_entities.people?.length > 0 && (
                <div className="entity-group">
                  <strong>People:</strong>
                  <div className="entity-tags">
                    {quizData.key_entities.people.map((person, i) => (
                      <span key={i} className="entity-tag">{person}</span>
                    ))}
                  </div>
                </div>
              )}
              {quizData.key_entities.organizations?.length > 0 && (
                <div className="entity-group">
                  <strong>Organizations:</strong>
                  <div className="entity-tags">
                    {quizData.key_entities.organizations.map((org, i) => (
                      <span key={i} className="entity-tag">{org}</span>
                    ))}
                  </div>
                </div>
              )}
              {quizData.key_entities.locations?.length > 0 && (
                <div className="entity-group">
                  <strong>Locations:</strong>
                  <div className="entity-tags">
                    {quizData.key_entities.locations.map((loc, i) => (
                      <span key={i} className="entity-tag">{loc}</span>
                    ))}
                  </div>
                </div>
              )}
            </div>
          </div>
        )}

        {/* Sections */}
        {quizData.sections?.length > 0 && (
          <div className="sections-list">
            <h3 className="subsection-title">Article Sections</h3>
            <div className="section-tags">
              {quizData.sections.map((section, i) => (
                <span key={i} className="section-tag">{section}</span>
              ))}
            </div>
          </div>
        )}
      </div>

      {/* Score Display (if quiz is submitted) */}
      {submitted && score && (
        <div className="score-card card">
          <div className="score-header">
            <Award size={32} className="score-icon" />
            <h3>Your Score</h3>
          </div>
          <div className="score-display">
            <div className="score-number">{score.percentage}%</div>
            <div className="score-details">
              {score.correct} out of {score.total} correct
            </div>
          </div>
          <button className="btn btn-primary" onClick={handleReset}>
            Try Again
          </button>
        </div>
      )}

      {/* Quiz Questions */}
      <div className="quiz-section">
        <div className="quiz-header">
          <h3 className="subsection-title">
            Quiz Questions ({quizData.quiz?.length || 0})
          </h3>
          {quizMode && !submitted && Object.keys(userAnswers).length > 0 && (
            <button className="btn btn-primary" onClick={handleSubmit}>
              Submit Quiz
            </button>
          )}
        </div>

        <div className="questions-list">
          {quizData.quiz?.map((question, index) => (
            <div key={index} className="question-card card">
              <div className="question-header">
                <span className="question-number">Question {index + 1}</span>
                <span className={`badge ${getDifficultyColor(question.difficulty)}`}>
                  {question.difficulty}
                </span>
              </div>

              <p className="question-text">{question.question}</p>

              <div className="options-list">
                {question.options?.map((option, optIndex) => {
                  const isCorrect = option === question.answer
                  const isSelected = userAnswers[index] === option
                  const showResult = submitted || !quizMode
                  
                  let optionClass = 'option'
                  if (quizMode && isSelected && !submitted) {
                    optionClass += ' option-selected'
                  }
                  if (showResult) {
                    if (isCorrect) {
                      optionClass += ' option-correct'
                    } else if (isSelected && !isCorrect) {
                      optionClass += ' option-incorrect'
                    }
                  }

                  return (
                    <button
                      key={optIndex}
                      className={optionClass}
                      onClick={() => handleAnswerSelect(index, option)}
                      disabled={!quizMode || submitted}
                    >
                      <span className="option-label">{String.fromCharCode(65 + optIndex)}.</span>
                      <span className="option-text">{option}</span>
                      {showResult && isCorrect && (
                        <CheckCircle className="option-icon" size={20} />
                      )}
                      {showResult && isSelected && !isCorrect && (
                        <XCircle className="option-icon" size={20} />
                      )}
                    </button>
                  )
                })}
              </div>

              {(!quizMode || submitted) && (
                <div className="explanation">
                  <strong>Explanation:</strong> {question.explanation}
                </div>
              )}
            </div>
          ))}
        </div>
      </div>

      {/* Related Topics */}
      {quizData.related_topics?.length > 0 && (
        <div className="related-topics card">
          <h3 className="subsection-title">Related Topics for Further Reading</h3>
          <div className="topics-grid">
            {quizData.related_topics.map((topic, i) => (
              <a
                key={i}
                href={`https://en.wikipedia.org/wiki/${topic.replace(/ /g, '_')}`}
                target="_blank"
                rel="noopener noreferrer"
                className="topic-link"
              >
                {topic} <ExternalLink size={14} />
              </a>
            ))}
          </div>
        </div>
      )}
    </div>
  )
}

export default QuizDisplay
