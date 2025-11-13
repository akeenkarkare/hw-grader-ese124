import { useState } from 'react'
import './TestCaseForm.css'

const TestCaseForm = ({ onSubmit, isHidden = false }) => {
  const [input, setInput] = useState('')
  const [expectedOutput, setExpectedOutput] = useState('')

  const handleSubmit = (e) => {
    e.preventDefault()
    if (input.trim() && expectedOutput.trim()) {
      onSubmit({ input, expected_output: expectedOutput, is_hidden: isHidden })
      setInput('')
      setExpectedOutput('')
    }
  }

  return (
    <form onSubmit={handleSubmit} className="test-case-form">
      <div className="form-group">
        <label className="form-label">Input:</label>
        <textarea
          value={input}
          onChange={(e) => setInput(e.target.value)}
          className="form-textarea"
          rows="3"
          required
        />
      </div>
      <div className="form-group">
        <label className="form-label">Expected Output:</label>
        <textarea
          value={expectedOutput}
          onChange={(e) => setExpectedOutput(e.target.value)}
          className="form-textarea"
          rows="3"
          required
        />
      </div>
      <button type="submit" className="btn btn-success">
        Add Test Case
      </button>
    </form>
  )
}

export default TestCaseForm

