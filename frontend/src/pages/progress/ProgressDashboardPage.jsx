import { useEffect, useState } from 'react';
import { Link } from 'react-router-dom';
import api from '../../api/axios';
import '../assessment.css';

function Bar({ label, percent }) {
  return (
    <div className="a-cat">
      <div className="a-head"><span>{label}</span><span>{percent}%</span></div>
      <div className="a-track"><div className="a-fill" style={{ width: `${percent}%` }} /></div>
    </div>
  );
}

export default function ProgressDashboardPage() {
  const [data, setData] = useState(null);
  const [error, setError] = useState('');

  useEffect(() => {
    api.get('progress/')
      .then((res) => setData(res.data))
      .catch(() => setError('Could not load your progress.'));
  }, []);

  if (error) return <div className="a-page"><p className="a-err">{error}</p></div>;
  if (!data) return <div className="a-page"><p className="a-muted">Loading...</p></div>;

  const { overall, aptitude, interview, roadmap, skills, achievements } = data;

  return (
    <div className="a-page">
      <h1>Progress Dashboard</h1>

      <div className="a-card">
        <p className="a-label">Overall Progress</p>
        <p className="a-big">{overall}%</p>
        <div className="a-track"><div className="a-fill" style={{ width: `${overall}%` }} /></div>
      </div>

      <div className="a-grid">
        <div className="a-box"><span>Aptitude (latest)</span>
          <strong>{aptitude.latest_percent !== null ? `${aptitude.latest_percent}%` : '-'}</strong></div>
        <div className="a-box"><span>Interview (average)</span>
          <strong>{interview.average_score !== null ? `${interview.average_score} / 10` : '-'}</strong></div>
        <div className="a-box"><span>Roadmap</span>
          <strong>{roadmap.percent !== null ? `${roadmap.percent}%` : 'Coming soon'}</strong></div>
      </div>

      <div className="a-card">
        <h3 style={{ marginBottom: 12 }}>Aptitude by category</h3>
        {aptitude.categories.length === 0 ? (
          <p className="a-muted">No test yet. <Link to="/aptitude">Take the aptitude test</Link></p>
        ) : (
          aptitude.categories.map((c) => <Bar key={c.category} label={c.category} percent={c.percentage} />)
        )}
      </div>

      <div className="a-card">
        <h3 style={{ marginBottom: 12 }}>Interview</h3>
        {interview.attempts === 0 ? (
          <p className="a-muted">No interview yet. <Link to="/interview">Start a mock interview</Link></p>
        ) : (
          <p>{interview.attempts} interview(s) completed. Latest score: <strong>{interview.latest_score} / 10</strong></p>
        )}
      </div>

      <div className="a-card">
        <h3 style={{ marginBottom: 4 }}>Skills</h3>
        <p className="a-muted">Sample data until the Skills module is connected.</p>
        {skills.map((s) => <Bar key={s.name} label={s.name} percent={s.percent} />)}
      </div>

      <div className="a-card">
        <h3 style={{ marginBottom: 12 }}>Achievements</h3>
        {achievements.map((a) => (
          <span key={a.title} className={`a-badge ${a.earned ? 'on' : ''}`}>
            {a.earned ? '🏆 ' : '🔒 '}{a.title}
          </span>
        ))}
      </div>
    </div>
  );
}