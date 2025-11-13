import { useState, useEffect } from 'react'
import axios from 'axios'
import Navbar from '../components/Navbar'
import TestCaseForm from '../components/TestCaseForm'
import TestCaseList from '../components/TestCaseList'
import './AdminDashboard.css'

const AdminDashboard = () => {
  const [problems, setProblems] = useState([])
  const [selectedProblem, setSelectedProblem] = useState(null)
  const [showProblemForm, setShowProblemForm] = useState(false)
  const [showTestCaseForm, setShowTestCaseForm] = useState(false)
  const [testCaseType, setTestCaseType] = useState('visible')
  const [loading, setLoading] = useState(true)

  const [problemForm, setProblemForm] = useState({
    title: '',
    description: '',
    difficulty: 'easy',
    constraints: '',
  })

  useEffect(() => {
    fetchProblems()
  }, [])

  const fetchProblems = async () => {
    try {
      const response = await axios.get('/api/admin/problems')
      setProblems(response.data)
    } catch (err) {
      console.error('Failed to fetch problems:', err)
      alert('Failed to fetch problems')
    } finally {
      setLoading(false)
    }
  }

  const handleCreateProblem = async (e) => {
    e.preventDefault()
    try {
      await axios.post('/api/admin/problems', problemForm)
      setProblemForm({
        title: '',
        description: '',
        difficulty: 'easy',
        constraints: '',
      })
      setShowProblemForm(false)
      fetchProblems()
    } catch (err) {
      console.error('Failed to create problem:', err)
      alert('Failed to create problem')
    }
  }

  const handleDeleteProblem = async (problemId) => {
    if (!confirm('Are you sure you want to delete this problem?')) return

    try {
      await axios.delete(`/api/admin/problems/${problemId}`)
      fetchProblems()
      if (selectedProblem?.id === problemId) {
        setSelectedProblem(null)
      }
    } catch (err) {
      console.error('Failed to delete problem:', err)
      alert('Failed to delete problem')
    }
  }

  const handleAddTestCase = async (testCaseData) => {
    if (!selectedProblem) return

    try {
      await axios.post(`/api/admin/problems/${selectedProblem.id}/testcases`, {
        ...testCaseData,
        is_hidden: testCaseType === 'hidden',
        display_order: selectedProblem.test_cases.length + 1,
      })
      // Refresh the selected problem
      const response = await axios.get(`/api/admin/problems/${selectedProblem.id}`)
      setSelectedProblem(response.data)
      fetchProblems()
      setShowTestCaseForm(false)
    } catch (err) {
      console.error('Failed to add test case:', err)
      alert('Failed to add test case')
    }
  }

  const handleDeleteTestCase = async (testCaseId) => {
    if (!confirm('Are you sure you want to delete this test case?')) return

    try {
      await axios.delete(`/api/admin/testcases/${testCaseId}`)
      // Refresh the selected problem
      const response = await axios.get(`/api/admin/problems/${selectedProblem.id}`)
      setSelectedProblem(response.data)
      fetchProblems()
    } catch (err) {
      console.error('Failed to delete test case:', err)
      alert('Failed to delete test case')
    }
  }

  const selectProblem = async (problemId) => {
    try {
      const response = await axios.get(`/api/admin/problems/${problemId}`)
      setSelectedProblem(response.data)
    } catch (err) {
      console.error('Failed to fetch problem details:', err)
      alert('Failed to fetch problem details')
    }
  }

  if (loading) {
    return (
      <>
        <Navbar />
        <div className="loading">Loading...</div>
      </>
    )
  }

  return (
    <>
      <Navbar />
      <div className="admin-dashboard">
        <div className="admin-sidebar">
          <div className="sidebar-header">
            <h2>Problems</h2>
            <button
              onClick={() => setShowProblemForm(!showProblemForm)}
              className="btn btn-primary btn-sm"
            >
              {showProblemForm ? 'Cancel' : 'New Problem'}
            </button>
          </div>

          {showProblemForm && (
            <form onSubmit={handleCreateProblem} className="problem-form">
              <div className="form-group">
                <label className="form-label">Title</label>
                <input
                  type="text"
                  value={problemForm.title}
                  onChange={(e) =>
                    setProblemForm({ ...problemForm, title: e.target.value })
                  }
                  className="form-input"
                  required
                />
              </div>

              <div className="form-group">
                <label className="form-label">Description (Markdown)</label>
                <textarea
                  value={problemForm.description}
                  onChange={(e) =>
                    setProblemForm({ ...problemForm, description: e.target.value })
                  }
                  className="form-textarea"
                  rows="5"
                  required
                />
              </div>

              <div className="form-group">
                <label className="form-label">Difficulty</label>
                <select
                  value={problemForm.difficulty}
                  onChange={(e) =>
                    setProblemForm({ ...problemForm, difficulty: e.target.value })
                  }
                  className="form-select"
                >
                  <option value="easy">Easy</option>
                  <option value="medium">Medium</option>
                  <option value="hard">Hard</option>
                </select>
              </div>

              <div className="form-group">
                <label className="form-label">Constraints</label>
                <input
                  type="text"
                  value={problemForm.constraints}
                  onChange={(e) =>
                    setProblemForm({ ...problemForm, constraints: e.target.value })
                  }
                  className="form-input"
                />
              </div>

              <button type="submit" className="btn btn-success">
                Create Problem
              </button>
            </form>
          )}

          <div className="problem-list">
            {problems.map((problem) => (
              <div
                key={problem.id}
                className={`problem-list-item ${
                  selectedProblem?.id === problem.id ? 'active' : ''
                }`}
                onClick={() => selectProblem(problem.id)}
              >
                <div className="problem-list-item-header">
                  <h4>{problem.title}</h4>
                  <span className={`badge badge-${problem.difficulty.toLowerCase()}`}>
                    {problem.difficulty}
                  </span>
                </div>
                <div className="problem-list-item-footer">
                  <span>{problem.test_cases?.length || 0} test cases</span>
                  <button
                    onClick={(e) => {
                      e.stopPropagation()
                      handleDeleteProblem(problem.id)
                    }}
                    className="btn btn-danger btn-sm"
                  >
                    Delete
                  </button>
                </div>
              </div>
            ))}
          </div>
        </div>

        <div className="admin-content">
          {selectedProblem ? (
            <>
              <div className="content-header">
                <h1>{selectedProblem.title}</h1>
                <span className={`badge badge-${selectedProblem.difficulty.toLowerCase()}`}>
                  {selectedProblem.difficulty}
                </span>
              </div>

              <div className="content-section">
                <h3>Description</h3>
                <div className="description-box">
                  <pre>{selectedProblem.description}</pre>
                </div>
              </div>

              {selectedProblem.constraints && (
                <div className="content-section">
                  <h3>Constraints</h3>
                  <p>{selectedProblem.constraints}</p>
                </div>
              )}

              <div className="content-section">
                <div className="section-header">
                  <h3>Test Cases</h3>
                  <div className="test-case-controls">
                    <select
                      value={testCaseType}
                      onChange={(e) => setTestCaseType(e.target.value)}
                      className="form-select"
                      style={{ width: 'auto', marginRight: '1rem' }}
                    >
                      <option value="visible">Visible</option>
                      <option value="hidden">Hidden</option>
                    </select>
                    <button
                      onClick={() => setShowTestCaseForm(!showTestCaseForm)}
                      className="btn btn-primary btn-sm"
                    >
                      {showTestCaseForm ? 'Cancel' : 'Add Test Case'}
                    </button>
                  </div>
                </div>

                {showTestCaseForm && (
                  <TestCaseForm
                    onSubmit={handleAddTestCase}
                    isHidden={testCaseType === 'hidden'}
                  />
                )}

                <div className="test-case-sections">
                  <div className="test-case-group">
                    <h4>
                      Visible Test Cases (
                      {selectedProblem.test_cases.filter((tc) => !tc.is_hidden).length})
                    </h4>
                    <TestCaseList
                      testCases={selectedProblem.test_cases.filter((tc) => !tc.is_hidden)}
                      onDelete={handleDeleteTestCase}
                      canDelete={true}
                    />
                  </div>

                  <div className="test-case-group">
                    <h4>
                      Hidden Test Cases (
                      {selectedProblem.test_cases.filter((tc) => tc.is_hidden).length})
                    </h4>
                    <TestCaseList
                      testCases={selectedProblem.test_cases.filter((tc) => tc.is_hidden)}
                      onDelete={handleDeleteTestCase}
                      canDelete={true}
                    />
                  </div>
                </div>
              </div>
            </>
          ) : (
            <div className="no-selection">
              <p>Select a problem from the sidebar to view and edit details</p>
            </div>
          )}
        </div>
      </div>
    </>
  )
}

export default AdminDashboard

