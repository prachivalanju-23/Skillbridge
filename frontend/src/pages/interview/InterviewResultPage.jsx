import { useEffect, useState } from 'react';
import { useParams, Link } from 'react-router-dom';
import api from '../../api/axios';
import '../assessment.css';

export default function InterviewResultPage() {
  const { id } = useParams();
  const [data, setData] = useState(null);
  const [error, setError] = useState('');

  useEffect(() => {
    api.get(`interview/result/${id}/`)
      .then((res) => setData(res.data))
      .catch(() => setError('Could not load the result.'));
  }, [id]);

  if (error) return <div className="a-page"><p className="a-err">{error}</p></div>;
  if (!data) return <div className="a-page"><p className="a-muted">Loading...</p></div>;

  const { result, questions } = data;

  return (
    <div className="a-page">
      <h1>Interview Result</h1>
      <div className="a-card">
        <p className="a-muted">{result.role} · {result.level}</p>
        <p className="a-label">Overall Score</p>
        <p className="a-big">{result.overall_score}/10</p>
        <div className="a-grid">
          <div className="a-box"><span>Technical</span><strong>{result.technical}/10</strong></div>
          <div className="a-box"><span>Communication</span><strong>{result.communication}/10</strong></div>
          <div className="a-box"><span>Accuracy</span><strong>{result.accuracy}/10</strong></div>
        </div>
        <p style={{ marginTop: 14 }}>{result.summary}</p>
        <h3 style={{ margin: '22px 0 10px' }}>Question review</h3>
        {questions.map((q, i) => (
          <div key={i} className="a-item">
            <p><strong>Q{i + 1}. {q.text}</strong> <span className="a-tag">{q.score}/10</span></p>
            <p className="a-muted">Your answer: {q.answer_text}</p>
            <p className="a-muted">Feedback: {q.feedback}</p>
          </div>
        ))}
        <div className="a-nav">
          <span />
          <Link className="a-btn" to="/interview">New Interview</Link>
        </div>
      </div>
    </div>
  );
}