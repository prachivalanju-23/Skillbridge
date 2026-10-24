import { Routes, Route, Navigate } from 'react-router-dom';
import { useAuth } from './context/AuthContext';
import Layout from './components/Layout';
import ProtectedRoute from './components/ProtectedRoute';
import LoginPage from './pages/auth/LoginPage';
import RegisterPage from './pages/auth/RegisterPage';
import ForgotPasswordPage from './pages/auth/ForgotPasswordPage';
import ResetPasswordPage from './pages/auth/ResetPasswordPage';
// Each member adds ONLY their own page imports below

// Member 1 (Prachi): resume, skill gap, profile
import ResumeUploadPage from './pages/resume/ResumeUploadPage';
import ResumeAnalysisPage from './pages/resume/ResumeAnalysisPage';
import SkillGapPage from './pages/resume/SkillGapPage';
import ProfilePage from './pages/resume/ProfilePage';

// Member 2 (Pradnya): career goal, roadmap, jobs
import CareerGoalPage from './pages/CareerGoalPage';
import RoadmapPage from './pages/RoadmapPage';
import JobsPage from './pages/JobsPage';
import JobDetailsPage from './pages/JobDetailsPage';

// Member 3 (Nikita): aptitude, interview, progress
import AptitudeTestPage from './pages/aptitude/AptitudeTestPage';
import AptitudeResultPage from './pages/aptitude/AptitudeResultPage';
import InterviewSelectPage from './pages/interview/InterviewSelectPage';
import InterviewChatPage from './pages/interview/InterviewChatPage';
import InterviewResultPage from './pages/interview/InterviewResultPage';
import ProgressDashboardPage from './pages/progress/ProgressDashboardPage';

// Opening the website goes to the profile when logged in, to login otherwise
function HomeRedirect() {
  const { isLoggedIn } = useAuth();
  return <Navigate to={isLoggedIn ? '/profile' : '/login'} replace />;
}

export default function App() {
  return (
    <Routes>
      <Route path="/" element={<HomeRedirect />} />

      {/* Public pages: shown full screen, without the sidebar */}
      <Route path="/login" element={<LoginPage />} />
      <Route path="/register" element={<RegisterPage />} />
      <Route path="/forgot-password" element={<ForgotPasswordPage />} />
      <Route path="/reset-password/:uid/:token" element={<ResetPasswordPage />} />

      {/* Logged-in pages are shown inside the sidebar Layout.
          Each member adds ONLY their own routes inside this block. */}
      <Route
        element={
          <ProtectedRoute>
            <Layout />
          </ProtectedRoute>
        }
      >
        {/* Member 1 (Prachi) */}
        <Route path="/resume-upload" element={<ResumeUploadPage />} />
        <Route path="/resume-analysis" element={<ResumeAnalysisPage />} />
        <Route path="/skill-gap" element={<SkillGapPage />} />
        <Route path="/profile" element={<ProfilePage />} />

        {/* Member 2 (Pradnya) */}
        <Route path="/careers" element={<CareerGoalPage />} />
        <Route path="/roadmap" element={<RoadmapPage />} />
        <Route path="/jobs" element={<JobsPage />} />
        <Route path="/jobs/:id" element={<JobDetailsPage />} />

        {/* Member 3 (Nikita) */}
        <Route path="/aptitude" element={<AptitudeTestPage />} />
        <Route path="/aptitude/result" element={<AptitudeResultPage />} />
        <Route path="/interview" element={<InterviewSelectPage />} />
        <Route path="/interview/session" element={<InterviewChatPage />} />
        <Route path="/interview/result/:id" element={<InterviewResultPage />} />
        <Route path="/progress" element={<ProgressDashboardPage />} />
      </Route>

      <Route path="*" element={<HomeRedirect />} />
    </Routes>
  );
}