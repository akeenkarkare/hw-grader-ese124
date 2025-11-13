import { BrowserRouter as Router, Routes, Route, Navigate } from 'react-router-dom'
import { AuthProvider } from './context/AuthContext'
import LoginPage from './pages/LoginPage'
import AdminDashboard from './pages/AdminDashboard'
import ProblemList from './pages/ProblemList'
import ProblemSolver from './pages/ProblemSolver'
import ProtectedRoute from './components/ProtectedRoute'
import './App.css'

function App() {
  return (
    <AuthProvider>
      <Router>
        <Routes>
          <Route path="/login" element={<LoginPage />} />
          <Route
            path="/admin"
            element={
              <ProtectedRoute requiredRole="admin">
                <AdminDashboard />
              </ProtectedRoute>
            }
          />
          <Route
            path="/problems"
            element={
              <ProtectedRoute>
                <ProblemList />
              </ProtectedRoute>
            }
          />
          <Route
            path="/problems/:id"
            element={
              <ProtectedRoute>
                <ProblemSolver />
              </ProtectedRoute>
            }
          />
          <Route path="/" element={<Navigate to="/problems" replace />} />
        </Routes>
      </Router>
    </AuthProvider>
  )
}

export default App

