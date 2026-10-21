import { Routes, Route } from 'react-router-dom';
import Navbar from './components/Navbar';
import ProtectedRoute from './components/ProtectedRoute';
import LoginPage from './pages/auth/LoginPage';
import RegisterPage from './pages/auth/RegisterPage';
import JobsPage from './pages/JobsPage';

import ResumeUploadPage from './pages/resume/ResumeUploadPage';
import ResumeAnalysisPage from './pages/resume/ResumeAnalysisPage';
import SkillGapPage from './pages/resume/SkillGapPage';
import ProfilePage from './pages/resume/ProfilePage';
import ForgotPasswordPage from './pages/auth/ForgotPasswordPage';
import ResetPasswordPage from './pages/auth/ResetPasswordPage';
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

                <Route path="/resume-upload" element={<ProtectedRoute><ResumeUploadPage /></ProtectedRoute>} />
        <Route path="/resume-analysis" element={<ProtectedRoute><ResumeAnalysisPage /></ProtectedRoute>} />
        <Route path="/skill-gap" element={<ProtectedRoute><SkillGapPage /></ProtectedRoute>} />
        <Route path="/profile" element={<ProtectedRoute><ProfilePage /></ProtectedRoute>} />
        <Route path="/forgot-password" element={<ForgotPasswordPage />} />
        <Route path="/reset-password/:uid/:token" element={<ResetPasswordPage />} />
        {/* Each member adds ONLY their own routes below, wrapped like this:
        <Route path="/profile" element={<ProtectedRoute><ProfilePage /></ProtectedRoute>} />
        */}
      </Routes>
    </>
  );
}