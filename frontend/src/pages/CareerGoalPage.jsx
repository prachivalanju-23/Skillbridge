import { useEffect, useState } from 'react';
import { Link } from 'react-router-dom';
import {
  Layers,
  Monitor,
  Server,
  TrendingUp,
  Brain,
  Briefcase,
  Check,
} from 'lucide-react';
import api from '../api';
import './careers.css';

const STORAGE_KEY = 'skillbridge_career_goal';

// maps the icon name sent by the backend to a real icon
const icons = { Layers, Monitor, Server, BarChart3: TrendingUp, Brain };

const loadSavedGoal = () => {
  try {
    return localStorage.getItem(STORAGE_KEY) || '';
  } catch {
    return '';
  }
};

export default function CareerGoalPage() {
  const [careers, setCareers] = useState([]);
  const [selectedId, setSelectedId] = useState(loadSavedGoal());
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');

  useEffect(() => {
    api
      .get('/careers')
      .then((res) => setCareers(res.data))
      .catch(() => setError('Could not load careers. Is the backend running?'))
      .finally(() => setLoading(false));
  }, []);

  const chooseCareer = (id) => {
    setSelectedId(id);
    try {
      localStorage.setItem(STORAGE_KEY, id);
    } catch {
      // storage not available, the choice just won't be remembered
    }
    api.post('/roadmap/goal', { career_id: id }).catch(() => {});
  };

  const selectedCareer = careers.find((c) => c._id === selectedId);

  return (
    <div className="page">
      <h1>Choose your career goal</h1>
      <p className="message">
        Pick the career you want to grow into. We use it to suggest jobs and build
        your learning roadmap.
      </p>

      {selectedCareer && (
        <div className="goal-banner">
          <div>
            <span>Your current goal</span>
            <h2>{selectedCareer.name}</h2>
          </div>
          <Link
            className="goal-banner-btn"
            to={`/jobs?category=${encodeURIComponent(selectedCareer.name)}`}
          >
            See matching jobs
          </Link>
        </div>
      )}

      {loading && <p className="message">Loading careers...</p>}
      {error && <p className="message error">{error}</p>}

      <div className="career-grid">
        {careers.map((career) => {
          const Icon = icons[career.icon] || Briefcase;
          const isSelected = career._id === selectedId;

          return (
            <button
              type="button"
              key={career._id}
              className={`career-card ${isSelected ? 'selected' : ''}`}
              style={{ background: career.color }}
              onClick={() => chooseCareer(career._id)}
            >
              {isSelected && (
                <span className="career-check">
                  <Check size={16} />
                </span>
              )}
              <span className="career-icon">
                <Icon size={24} />
              </span>
              <h3>{career.name}</h3>
              <p>{career.description}</p>
              <div className="skills">
                {career.requiredSkills.slice(0, 5).map((skill) => (
                  <span className="skill-tag" key={skill}>
                    {skill}
                  </span>
                ))}
              </div>
              <span className="career-select-label">
                {isSelected ? 'Selected goal' : 'Select this goal'}
              </span>
            </button>
          );
        })}
      </div>
    </div>
  );
}