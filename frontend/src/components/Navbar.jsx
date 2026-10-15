import { NavLink, useNavigate } from 'react-router-dom';
import { useAuth } from '../context/AuthContext';

export default function Navbar() {
  const { isLoggedIn, logout } = useAuth();
  const navigate = useNavigate();

  return (
    <nav className="navbar">
      <span className="brand">SkillBridge</span>
      <div className="links">
        <NavLink to="/">Home</NavLink>
        <NavLink to="/jobs">Jobs</NavLink>

        {isLoggedIn ? (
          <>
            {/* Each member adds ONLY their own links below */}
            {/* Member 1: Resume, Skill Gap, Profile (Prachi adds these later) */}
            {/* Member 2: Roadmap */}
            {/* Member 3: Interview, Aptitude, Progress */}
            <a href="/login" onClick={(e) => { e.preventDefault(); logout(); navigate('/login'); }}>
              Logout
            </a>
          </>
        ) : (
          <>
            <NavLink to="/login">Login</NavLink>
            <NavLink to="/register">Register</NavLink>
          </>
        )}
      </div>
    </nav>
  );
}