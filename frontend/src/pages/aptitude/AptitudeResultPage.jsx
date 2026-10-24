import { useEffect, useState } from 'react';
import { useLocation, Link } from 'react-router-dom';
import api from '../../api/axios';
import '../assessment.css';

export default function AptitudeResultPage() {
  const location = useLocation();
  const [result, setResult] = useState(location.state?.result || null);
  const [loading, setLoading] = useState(!location.state?.result);
  const [error, setError] = useState('');

  useEffect(() => {
    if (result) return;
    api.get('aptitude/results/')
      .then((res) => setResult(res.data[0] || null))
      .catch(() => setError('Could not load your result.'))
      .finally(() => setLoading(false));
  }, [result]);

  if (loading) return <div className="a-page"><p className="a-muted">Loading...</p></div>;
  if (error) return <div className="a-page"><p className="a-err">{error}</p></div>;
  if (!result) {
    return (
      <div className="a-page">
        <p className="a-muted">No results yet.</p>
        <Link className="a-btn" to="/aptitude">Take the test</Link>
      </div>
    );
  }

  const percent = Math.round((result.score / result.total) * 100);

  return (
    <div className="a-page">
      <h1>Aptitude Result</h1>
      <div className="a-card">
        <p className="a-label">Aptitude Score</p>
        <p className="a-big">{result.score}/{result.total}</p>
        <p className="a-muted">{percent}% overall</p>
        <h3 style={{ margin: '20px 0 10px' }}>Category breakdown</h3>
        {result.category_scores.map((c) => (
          <div key={c.category} className="a-cat">
            <div className="a-head">
              <span>{c.category}</span>
              <span>{c.percentage}% ({c.correct}/{c.total})</span>
            </div>
            <div className="a-track"><div className="a-fill" style={{ width: `${c.percentage}%` }} /></div>
          </div>
        ))}
        <div className="a-nav">
          <span />
          <Link className="a-btn" to="/aptitude">Retake Test</Link>
        </div>
      </div>
    </div>
  );
}