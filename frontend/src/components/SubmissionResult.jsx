"use client"
import './SubmissionResult.css'
import React, { useEffect, useState } from 'react'
import {createPortal} from 'react-dom'

const SubmissionResult = ({ submission, clearCurrentSubmission}) => {
  if (!submission) return null;
  
  // Handle both JSON object (new) and JSON string (old)
  const results = typeof submission.results === 'string'
    ? JSON.parse(submission.results)
    : submission.results || []

  const hasError = submission.status === 'error' || results.error
  const isCompilationError = submission.status === 'compilation_error'
  return createPortal((
    <div className="submission-result ">
      <div className="result-header">
        <h3>Submission Result</h3>
        <div className='spacer'></div>
        <div className="score">
          Score: <span className={`score-value ${submission.score === 100 ? 'perfect-score' : ''}`}>
            {submission.score.toFixed(1)}%
          </span>
        </div>
        <button className = "close-button"onClick={clearCurrentSubmission}>X</button>
      </div>
      

      {isCompilationError && (
        <div className="alert alert-error">
          <strong>Compilation Error:</strong> Your code failed to compile. Check the details below.
        </div>
      )}

      {hasError && !isCompilationError && (
        <div className="alert alert-error">
          <strong>Error:</strong> {results.error || 'Unknown error occurred'}
        </div>
      )}

      {!hasError && Array.isArray(results) && (
        <div className="test-results">
          <h4>Test Results ({results.filter(r => r.passed).length}/{results.length} passed)</h4>
          <div className="test-results-list">
            {results.map((result, index) => (
              <div key={index} className={`test-result-item ${result.passed ? 'passed' : 'failed'}`}>
                <div className="test-result-header">
                  <span className="test-number">Test {index + 1}</span>
                  <span className={`test-status ${result.passed ? 'status-passed' : 'status-failed'}`}>
                    {result.passed ? '✓ Passed' : '✗ Failed'}
                  </span>
                </div>
                
                {result.compile_output && (
                  <div className="test-detail">
                    <strong>Compilation Error:</strong>
                    <pre>{result.compile_output}</pre>
                  </div>
                )}
                
                {result.stderr && (
                  <div className="test-detail">
                    <strong>Runtime Error:</strong>
                    <pre>{result.stderr}</pre>
                  </div>
                )}
                
                {!result.passed && !result.compile_output && (
                  <div className='test-detail-container'>
                    <div className="test-detail">
                      <strong>Expected:</strong>
                      <pre>{result.expected_output}</pre>
                    </div>
                    <div className="test-detail">
                      <strong>Got:</strong>
                      <pre>{result.actual_output || '(no output)'}</pre>
                    </div>
                  </div>
                )}
                
                {result.time && (
                  <div className="test-meta">
                    Time: {result.time}s | Memory: {result.memory} KB
                  </div>
                )}
              </div>
            ))}
          </div>
        </div>
      )}
    </div>
  ), document.body)
}

export default SubmissionResult

