import { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import api from '../../api/axios';
import '../assessment.css';

const ROLES = ['Frontend Developer', 'Backend Developer', 'Full Stack Developer', 'Data Analyst', 'AI/ML Engineer'];
const LEVELS = ['Beginner', 'Intermediate', 'Advanced'];

export default function InterviewSelectPage() {
  const navigate = useNavigate();
  const [role, setRole] = useState(ROLES[0]);
  const [level, setLevel] = useState(LEVELS[0]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');

  const start = async () => {
    setLoading(true);
    setError('');
    try {
      const res = await api.post('interview/start/', { role, level });
      navigate('/interview/session', { state: res.data });
    } catch {
      setError('Could not start the interview. Is the backend running?');
      setLoading(false);
    }
  };

  return (
    <div className="a-page">
      <h1>Mock Interview</h1>
      <p>Choose a role and level. You will answer 5 questions and get a score for each.</p>
      <div className="a-row">
        <select className="a-select" value={role} onChange={(e) => setRole(e.target.value)}>
          {ROLES.map((r) => <option key={r}>{r}</option>)}
        </select>
        <select className="a-select" value={level} onChange={(e) => setLevel(e.target.value)}>
          {LEVELS.map((l) => <option key={l}>{l}</option>)}
        </select>
        <button className="a-btn" onClick={start} disabled={loading}>
          {loading ? 'Starting...' : 'Start Interview'}
        </button>
      </div>
      {error && <p className="a-err">{error}</p>}
    </div>
  );
}