import { useState, useEffect } from 'react'
import { Link } from 'react-router-dom'
import axios from 'axios'
import Navbar from '../components/Navbar'
import './ProblemList.css'

const ProblemList = () => {
  const [problems, setProblems] = useState([])
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState('')

  useEffect(() => {
    fetchProblems()
  }, [])

  const fetchProblems = async () => {
    try {
      const response = await axios.get('/api/problems')
      setProblems(response.data)
    } catch (err) {
      setError('Failed to fetch problems')
      console.error(err)
    } finally {
      setLoading(false)
    }
  }

  const getDifficultyClass = (difficulty) => {
    return `badge badge-${difficulty.toLowerCase()}`
  }

  if (loading) {
    return (
      <>
        <Navbar />
        <div className="loading">Loading problems...</div>
      </>
    )
  }

  return (
    <>
      <Navbar />
      <div className="container">
        <div className="problem-list-header">
          <h1>Problems</h1>
          <p className="subtitle">Select a problem to start coding</p>
        </div>

        {error && (
          <div className="alert alert-error">{error}</div>
        )}

        <div className="problem-grid">
          {problems.map((problem) => (
            <Link
              key={problem.id}
              to={`/problems/${problem.id}`}
              className="problem-card-link"
            >
              <div className="problem-card">
                <div className="problem-card-header">
                  <h3>{problem.title}</h3>
                  <span className={getDifficultyClass(problem.difficulty)}>
                    {problem.difficulty}
                  </span>
                </div>
                <p className="problem-description-preview">
                  {problem.description.substring(0, 150)}...
                </p>
                <div className="problem-card-footer">
                  <span className="test-case-count">
                    {problem.visible_test_cases?.length || 0} visible test cases
                  </span>
                </div>
              </div>
            </Link>
          ))}
        </div>

        {problems.length === 0 && !error && (
          <div className="no-problems">
            <p>No problems available yet.</p>
            <p>Check back later or contact your instructor.</p>
          </div>
        )}
      </div>
    </>
  )
}

export default ProblemList

