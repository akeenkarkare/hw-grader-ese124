import { useState, useEffect } from 'react'
import { useParams, Link } from 'react-router-dom'
import axios from 'axios'
import ReactMarkdown from 'react-markdown'
import Navbar from '../components/Navbar'
import CodeEditor from '../components/CodeEditor'
import TestCaseList from '../components/TestCaseList'
import TestCaseForm from '../components/TestCaseForm'
import SubmissionResult from '../components/SubmissionResult'
import './ProblemSolver.css'
import FileExplorer from '@components/FileExplorer/FileExplorer'

const useCode = () => {
  const [files, setFiles] = useState(() => {
    return {
      source_code: '#include <stdio.h>\n\nint main() {\n    // Write your code here\n    \n    return 0;\n}',
      language_id: 89,
      compile: '',
      additional_files: [
        
      ]
    }
  });

  const submitFiles = async ()=>{
    // get the file code strings from "additional_files", convert them all to base64, and zip up the strings so that they are in aformat that can be used for judge0 api.
    
    const options = {}; // judge0 submission option
    const response = await axios.post('/api/submit', )
  }
  const clearFiles = async () => {}

}

const ProblemSolver = () => {
  const { id } = useParams()
  const [problem, setProblem] = useState(null)
  const [code, setCode] = useState('#include <stdio.h>\n\nint main() {\n    // Write your code here\n    \n    return 0;\n}')
  const [userTestCases, setUserTestCases] = useState([])
  const [submissions, setSubmissions] = useState([])
  const [currentSubmission, setCurrentSubmission] = useState(null)
  const [loading, setLoading] = useState(true)
  const [submitting, setSubmitting] = useState(false)
  const [error, setError] = useState('')
  const [showAddTestCase, setShowAddTestCase] = useState(false)
  const [autoSaveStatus, setAutoSaveStatus] = useState('')

  const [showFileViewer, setFileViewer] = useState(true);



  // Load code from localStorage on mount
  useEffect(() => {
    const savedCode = localStorage.getItem(`problem_${id}_code`);
    if (savedCode) {
      setCode(savedCode)
      setAutoSaveStatus('Loaded from auto-save')
      setTimeout(() => setAutoSaveStatus(''), 3000)
    }
  }, [id])

  // Auto-save code to localStorage
  useEffect(() => {
    if (code && problem) {
      const timeoutId = setTimeout(() => {
        localStorage.setItem(`problem_${id}_code`, code) // update
        setAutoSaveStatus('Auto-saved')
        setTimeout(() => setAutoSaveStatus(''), 2000)
      }, 1000)
      return () => clearTimeout(timeoutId)
    }
  }, [code, id, problem])

  useEffect(() => {
    fetchProblem()
    fetchUserTestCases()
    fetchSubmissions()
  }, [id])

  const fetchProblem = async () => {
    try {
      const response = await axios.get(`/api/problems/${id}`)
      setProblem(response.data)
    } catch (err) {
      setError('Failed to fetch problem')
      console.error(err)
    } finally {
      setLoading(false)
    }
  }
  
  const fetchUserTestCases = async () => {
    try {
      const response = await axios.get(`/api/problems/${id}/user-testcases`)
      setUserTestCases(response.data)
    } catch (err) {
      console.error('Failed to fetch user test cases:', err)
    }
  }

  const fetchSubmissions = async () => {
    try {
      const response = await axios.get(`/api/problems/${id}/submissions`)
      setSubmissions(response.data)
    } catch (err) {
      console.error('Failed to fetch submissions:', err)
    }
  }

  const handleAddUserTestCase = async (testCase) => {
    try {
      await axios.post('/api/user-testcases', {
        problem_id: parseInt(id),
        input: testCase.input,
        expected_output: testCase.expected_output,
      })
      fetchUserTestCases()
      setShowAddTestCase(false)
    } catch (err) {
      alert('Failed to add test case')
      console.error(err)
    }
  }

  const handleDeleteUserTestCase = async (testCaseId) => {
    if (!window.confirm('Are you sure you want to delete this test case?')) return

    try {
      await axios.delete(`/api/user-testcases/${testCaseId}`)
      fetchUserTestCases()
    } catch (err) {
      setError('Failed to delete test case')
      console.error(err)
      setTimeout(() => setError(''), 5000)
    }
  }

  const handleClearCode = () => {
    if (window.confirm('Are you sure you want to clear all code? This action cannot be undone.')) {
      const defaultCode = '#include <stdio.h>\n\nint main() {\n    // Write your code here\n    \n    return 0;\n}'
      setCode(defaultCode)
      localStorage.removeItem(`problem_${id}_code`)
    }
  }

  const handleSubmit = async () => {
    if (!code.trim()) {
      setError('Please write some code before submitting')
      setTimeout(() => setError(''), 5000)
      return
    }

    setSubmitting(true)
    setError('')

    try {
      const response = await axios.post('/api/submit', {
        problem_id: parseInt(id),
        code: code,
      })
      setCurrentSubmission(response.data)
      fetchSubmissions()

      // Show success message
      if (response.data.status === 'compilation_error') {
        setError('Compilation error - see results below')
      } else if (response.data.score === 100) {
        setError('Perfect score! All test cases passed!')
      }
      setTimeout(() => setError(''), 5000)
    } catch (err) {
      const errorMsg = err.response?.data?.detail || 'Submission failed. Please try again.'
      setError(errorMsg)
      console.error(err)
      setTimeout(() => setError(''), 8000)
    } finally {
      setSubmitting(false)
    }
  }

  const clearCurrentSubmission = () =>{ 
    setCurrentSubmission(null)};

  if (loading) {
    return (
      <>
        <Navbar />
        <div className="loading">Loading problem...</div>
      </>
    )
  }

  if (!problem) {
    return (
      <>
        <Navbar />
        <div className="container">
          <div className="alert alert-error">Problem not found</div>
          <Link to="/problems" className="btn btn-primary">
            Back to Problems
          </Link>
        </div>
      </>
    )
  }

  return (
    <>
      <Navbar />
      <div className="problem-solver">
        <div className="problem-panel">
          <div className="problem-header">
            <Link to="/problems" className="back-link">
              ← Back to Problems
            </Link>
            <h1>{problem.title}</h1>
            <span className={`badge badge-${problem.difficulty.toLowerCase()}`}>
              {problem.difficulty}
            </span>
          </div>

          <div className="problem-content">
            <div className="markdown-content">
              <ReactMarkdown>{problem.description}</ReactMarkdown>
            </div>

            {problem.constraints && (
              <div className="constraints">
                <h3>Constraints</h3>
                <p>{problem.constraints}</p>
              </div>
            )}

            <div className="test-cases-section">
              <h3>Visible Test Cases</h3>
              <TestCaseList
                testCases={problem.visible_test_cases || []}
                canDelete={false}
              />
            </div>

            <div className="user-test-cases-section">
              <div className="section-header">
                <h3>Your Custom Test Cases</h3>
                <button
                  onClick={() => setShowAddTestCase(!showAddTestCase)}
                  className="btn btn-primary btn-sm"
                >
                  {showAddTestCase ? 'Cancel' : 'Add Test Case'}
                </button>
              </div>

              {showAddTestCase && (
                <TestCaseForm onSubmit={handleAddUserTestCase} />
              )}

              <TestCaseList
                testCases={userTestCases}
                onDelete={handleDeleteUserTestCase}
                canDelete={true}
              />
            </div>

            {submissions.length > 0 && (
              <div className="submission-history">
                <h3>Your Submissions</h3>
                <div className="submission-list">
                  {submissions.slice(0, 5).map((sub) => (
                    <div key={sub.id} className="submission-item">
                      <span className="submission-date">
                        {new Date(sub.created_at).toLocaleString()}
                      </span>
                      <span className={`submission-score score-${sub.score >= 70 ? 'good' : sub.score >= 40 ? 'medium' : 'low'}`}>
                        {sub.score.toFixed(1)}%
                      </span>
                      <button
                        onClick={() => setCurrentSubmission(sub)}
                        className="btn btn-secondary btn-sm"
                      >
                        View Results
                      </button>
                    </div>
                  ))}
                </div>
              </div>
            )}
          </div>
        </div>
            {/* solutions */}
        <div className='flex flex-row h-full'>
          <FileExplorer/> 
          <div className="code-panel h-full grow-[2]">
          <div className="code-header">
            <div>
              <h2>Your Solution</h2>
              {autoSaveStatus && (
                <span style={{ fontSize: '12px', color: '#666', marginLeft: '10px' }}>
                  {autoSaveStatus}
                </span>
              )}
            </div>
            <div style={{ display: 'flex', gap: '10px' }}>
              <button
                onClick={handleClearCode}
                className="btn btn-secondary"
                disabled={submitting}
              >
                Clear Code
              </button>
              <button
                onClick={handleSubmit}
                disabled={submitting}
                className="btn btn-success"
              >
                {submitting ? 'Submitting...' : 'Submit Code'}
              </button>
            </div>
          </div>
            
          {error && (
            <div className={`alert ${error.includes('Perfect') ? 'alert-success' : 'alert-error'}`}>
              {error}
            </div>
          )}
          
          <CodeEditor
            value={code}
            onChange={(value) => setCode(value || '')}
            height="500px"
          />
            
         

          {currentSubmission && (
            <SubmissionResult submission={currentSubmission} clearCurrentSubmission={clearCurrentSubmission} />
          )}
        </div>
      </div>
      </div>
    </>
  )
}

export default ProblemSolver

