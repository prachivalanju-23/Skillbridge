import { NavLink, Outlet } from 'react-router-dom';
import { Briefcase, Target, Map as MapIcon, Brain, MessageSquare, BarChart3 } from 'lucide-react';
import '../design.css';

// Each member adds ONLY their own link in this list
const navItems = [
  { to: '/careers', label: 'Career Goal', icon: Target },
  { to: '/roadmap', label: 'Roadmap', icon: MapIcon },
  { to: '/jobs', label: 'Jobs', icon: Briefcase },
  // Member 3 (Nikita)
  { to: '/aptitude', label: 'Aptitude', icon: Brain },
  { to: '/interview', label: 'Interview', icon: MessageSquare },
  { to: '/progress', label: 'Progress', icon: BarChart3 },
];

export default function Layout() {
  return (
    <div className="app-shell">
      <aside className="sidebar">
        <div className="logo">
          <span className="logo-mark">S</span>
          <span className="logo-text">SkillBridge</span>
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
          <div className="avatar">S</div>
        </header>

        <main>
          <Outlet />
        </main>
      </div>
    </div>
  );
}