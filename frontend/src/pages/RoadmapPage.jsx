import { useEffect, useState } from 'react';
import { Link } from 'react-router-dom';
import { Check, Clock, ExternalLink } from 'lucide-react';
import api from '../api';
import './roadmap.css';

const GOAL_KEY = 'skillbridge_career_goal';
const SKILLS_KEY = 'skillbridge_skills';

const readStorage = (key) => {
  try {
    return localStorage.getItem(key) || '';
  } catch {
    return '';
  }
};

const writeStorage = (key, value) => {
  try {
    localStorage.setItem(key, value);
  } catch {
    // storage not available, the value just won't be remembered
  }
};

const weekLabel = (step) =>
  step.startWeek === step.endWeek
    ? `Week ${step.startWeek}`
    : `Weeks ${step.startWeek}–${step.endWeek}`;

export default function RoadmapPage() {
  const goalId = readStorage(GOAL_KEY);
  const [skillsInput, setSkillsInput] = useState(readStorage(SKILLS_KEY));
  const [appliedSkills, setAppliedSkills] = useState(readStorage(SKILLS_KEY));
  const [roadmap, setRoadmap] = useState(null);
  const [loading, setLoading] = useState(Boolean(goalId));
  const [error, setError] = useState('');

  useEffect(() => {
    if (!goalId) return;

    setLoading(true);
    setError('');

    api
      .get(`/roadmaps/career/${goalId}`, {
        params: appliedSkills ? { skills: appliedSkills } : {},
      })
      .then((res) => setRoadmap(res.data))
      .catch(() =>
        setError('Could not load the roadmap. Is the backend running?')
      )
      .finally(() => setLoading(false));
  }, [goalId, appliedSkills]);

  const handleSubmit = (e) => {
    e.preventDefault();
    const value = skillsInput.trim();
    writeStorage(SKILLS_KEY, value);
    setAppliedSkills(value);
  };

  const nextIndex = roadmap ? roadmap.steps.findIndex((s) => !s.done) : -1;

  return (
    <div className="page">
      <h1>Your Learning Roadmap</h1>
      <p className="message">
        A step-by-step plan to reach your career goal. Skills you already know are
        marked as done.
      </p>

      {!goalId && (
        <div className="empty-card">
          <h3>No career goal selected yet</h3>
          <p>Choose a career first, and we will build your roadmap.</p>
          <Link className="empty-btn" to="/careers">
            Choose your career goal
          </Link>
        </div>
      )}

      {goalId && (
        <form className="search-bar" onSubmit={handleSubmit}>
          <input
            type="text"
            placeholder="Skills you already know, e.g. HTML, CSS, JavaScript"
            value={skillsInput}
            onChange={(e) => setSkillsInput(e.target.value)}
          />
          <button type="submit">Update roadmap</button>
        </form>
      )}

      {loading && <p className="message">Building your roadmap...</p>}
      {error && <p className="message error">{error}</p>}

      {roadmap && (
        <>
          <div className="roadmap-hero">
            <span className="label">Your career goal</span>
            <h2>{roadmap.careerName}</h2>

            <div className="progress-track">
              <div
                className="progress-fill"
                style={{ width: `${roadmap.progressPercent}%` }}
              />
            </div>
            <p className="progress-text">{roadmap.progressPercent}% complete</p>

            <div className="roadmap-stats">
              <div className="stat-box">
                <strong>
                  {roadmap.completedSteps}/{roadmap.totalSteps}
                </strong>
                <span>Skills completed</span>
              </div>
              <div className="stat-box">
                <strong>{roadmap.totalWeeks}</strong>
                <span>Weeks to finish</span>
              </div>
              <div className="stat-box">
                <strong>{roadmap.totalMonths}</strong>
                <span>Months (approx.)</span>
              </div>
            </div>
          </div>

          <ol className="timeline">
            {roadmap.steps.map((step, i) => {
              const status = step.done
                ? 'done'
                : i === nextIndex
                ? 'next'
                : 'upcoming';
              const statusLabel =
                status === 'done'
                  ? 'Completed'
                  : status === 'next'
                  ? 'Up next'
                  : 'Upcoming';

              return (
                <li key={step.skill} className={`timeline-item ${status}`}>
                  <div className="timeline-marker">
                    {step.done ? <Check size={18} /> : step.order}
                  </div>

                  <div className="timeline-card">
                    <div className="timeline-head">
                      <h3>{step.skill}</h3>
                      <span className={`status-pill ${status}`}>{statusLabel}</span>
                    </div>

                    <p>{step.description}</p>

                    <div className="timeline-foot">
                      {!step.done && (
                        <span className="weeks">
                          <Clock size={15} /> {weekLabel(step)}
                        </span>
                      )}
                      {step.resourceUrl && (
                        <a
                          className="resource-link"
                          href={step.resourceUrl}
                          target="_blank"
                          rel="noreferrer"
                        >
                          {step.resourceTitle} <ExternalLink size={14} />
                        </a>
                      )}
                    </div>
                  </div>
                </li>
              );
            })}
          </ol>
        </>
      )}
    </div>
  );
}