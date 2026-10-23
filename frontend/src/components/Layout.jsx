import { NavLink, Outlet, useNavigate } from 'react-router-dom';
import { Briefcase, Target, Map as MapIcon, FileText, ListChecks, User } from 'lucide-react';
import Logo from './Logo';
import { useAuth } from '../context/AuthContext';
import '../design.css';
import './theme.css';
import './ui-polish.css';

// Each member adds ONLY their own link in this list
const navItems = [
  { to: '/resume-upload', label: 'Resume Upload', icon: FileText },
  { to: '/skill-gap', label: 'Skill Gap', icon: ListChecks },
  { to: '/profile', label: 'Profile', icon: User },
  { to: '/careers', label: 'Career Goal', icon: Target },
  { to: '/roadmap', label: 'Roadmap', icon: MapIcon },
  { to: '/jobs', label: 'Jobs', icon: Briefcase },
];

export default function Layout() {
  const { logout } = useAuth();
  const navigate = useNavigate();

  return (
    <div className="app-shell">
      <aside className="sidebar">
        <div className="logo">
          <Logo size={36} light />
        </div>

        <nav className="side-nav">
          {navItems.map(({ to, label, icon: Icon }) => (
            <NavLink key={to} to={to} className="side-link">
              <Icon size={19} />
              <span>{label}</span>
            </NavLink>
          ))}
        </nav>

        <div className="side-footer">AI Career &amp; Skill Platform</div>
      </aside>

      <div className="main-area">
        <header className="topbar">
          <span className="topbar-title">AI Career &amp; Skill Development Platform</span>
          <div style={{ display: 'flex', alignItems: 'center', gap: 12 }}>
            <button
              onClick={() => { logout(); navigate('/login'); }}
              style={{ background: '#fff', color: '#1d4ed8', border: '1px solid #bfdbfe', borderRadius: 10,
                       padding: '7px 16px', fontWeight: 600, cursor: 'pointer' }}
            >
              Logout
            </button>
            <div className="avatar">S</div>
          </div>
        </header>

        <main>
          <Outlet />
        </main>
      </div>
    </div>
  );
}