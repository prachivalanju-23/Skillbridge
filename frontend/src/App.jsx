import { Routes, Route } from 'react-router-dom';
import Navbar from './components/Navbar';
import ProtectedRoute from './components/ProtectedRoute';
import LoginPage from './pages/auth/LoginPage';
import RegisterPage from './pages/auth/RegisterPage';
import JobsPage from './pages/JobsPage';
// Each member adds ONLY their own page imports below

function Home() {
  return (
    <div className="page">
      <h1>SkillBridge</h1>
      <p>AI-Based Career &amp; Skill Development Platform</p>
    </div>
  );
}

export default function App() {
  return (
    <>
      <Navbar />
      <Routes>
        <Route path="/" element={<Home />} />
        <Route path="/login" element={<LoginPage />} />
        <Route path="/register" element={<RegisterPage />} />

        {/* Member 2's route (kept as it was) */}
        <Route path="/jobs" element={<JobsPage />} />

        {/* Each member adds ONLY their own routes below, wrapped like this:
        <Route path="/profile" element={<ProtectedRoute><ProfilePage /></ProtectedRoute>} />
        */}
      </Routes>
    </>
  );
}