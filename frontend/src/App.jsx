import { Routes, Route } from 'react-router-dom';
import Navbar from './components/Navbar';
import Layout from './components/Layout';
import ProtectedRoute from './components/ProtectedRoute';
import LoginPage from './pages/auth/LoginPage';
import RegisterPage from './pages/auth/RegisterPage';
// Each member adds ONLY their own page imports below
import CareerGoalPage from './pages/CareerGoalPage';
import RoadmapPage from './pages/RoadmapPage';
import JobsPage from './pages/JobsPage';
import JobDetailsPage from './pages/JobDetailsPage';
//member 3 import
import AptitudeTestPage from './pages/aptitude/AptitudeTestPage';
import AptitudeResultPage from './pages/aptitude/AptitudeResultPage';
import InterviewSelectPage from './pages/interview/InterviewSelectPage';
import InterviewChatPage from './pages/interview/InterviewChatPage';
import InterviewResultPage from './pages/interview/InterviewResultPage';
import ProgressDashboardPage from './pages/progress/ProgressDashboardPage';

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

        {/* Logged-in pages are shown inside the sidebar Layout.
            Each member adds ONLY their own routes inside this block. */}
        <Route
          element={
            <ProtectedRoute>
              <Layout />
            </ProtectedRoute>
          }
        >
          {/* Member 2 (Pradnya): career goal, roadmap and jobs */}
          <Route path="/careers" element={<CareerGoalPage />} />
          <Route path="/roadmap" element={<RoadmapPage />} />
          <Route path="/jobs" element={<JobsPage />} />
          <Route path="/jobs/:id" element={<JobDetailsPage />} />

          {/* Member 1 and Member 3: add your routes here, for example:
          <Route path="/profile" element={<ProfilePage />} /> */}
                    {/* Member 3 (Nikita): aptitude, interview and progress */}
          <Route path="/aptitude" element={<AptitudeTestPage />} />
          <Route path="/aptitude/result" element={<AptitudeResultPage />} />
          <Route path="/interview" element={<InterviewSelectPage />} />
          <Route path="/interview/session" element={<InterviewChatPage />} />
          <Route path="/interview/result/:id" element={<InterviewResultPage />} />
          <Route path="/progress" element={<ProgressDashboardPage />} />
        </Route>
      </Routes>
    </>
  );
}