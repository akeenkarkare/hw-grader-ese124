import './TestCaseList.css'

const TestCaseList = ({ testCases, onDelete, canDelete = false }) => {
  return (
    <div className="test-case-list">
      {testCases.map((tc, index) => (
        <div key={tc.id} className="test-case-item">
          <div className="test-case-header">
            <h4>Test Case {index + 1}</h4>
            {canDelete && (
              <button
                onClick={() => onDelete(tc.id)}
                className="btn btn-danger btn-sm"
              >
                Delete
              </button>
            )}
          </div>
          <div className="test-case-content">
            <div className="test-case-section">
              <strong>Input:</strong>
              <pre>{tc.input}</pre>
            </div>
            <div className="test-case-section">
              <strong>Expected Output:</strong>
              <pre>{tc.expected_output}</pre>
            </div>
          </div>
        </div>
      ))}
      {testCases.length === 0 && (
        <p className="no-test-cases">No test cases yet.</p>
      )}
    </div>
  )
}

export default TestCaseList

