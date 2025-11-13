import { Link } from 'react-router-dom'
import { useAuth } from '../context/AuthContext'

const Navbar = () => {
  const { user, logout } = useAuth()

  return (
    <nav className="navbar">
      <Link to="/" className="navbar-brand">
        Homework Grader
      </Link>
      <div className="navbar-menu">
        {user && (
          <>
            <Link to="/problems" className="navbar-link">
              Problems
            </Link>
            {user.role === 'admin' && (
              <Link to="/admin" className="navbar-link">
                Admin Dashboard
              </Link>
            )}
            <span className="navbar-user">
              {user.username} ({user.role})
            </span>
            <button onClick={logout} className="btn btn-secondary btn-sm">
              Logout
            </button>
          </>
        )}
      </div>
    </nav>
  )
}

export default Navbar

