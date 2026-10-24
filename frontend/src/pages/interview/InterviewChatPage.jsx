import { useState } from 'react';
import { useLocation, useNavigate, Navigate } from 'react-router-dom';
import api from '../../api/axios';
import '../assessment.css';

export default function InterviewChatPage() {
  const { state } = useLocation();
  const navigate = useNavigate();
  const [current, setCurrent] = useState(
    state ? { number: state.number, total: state.total, question: state.question } : null
  );
  const [answer, setAnswer] = useState('');
  const [reply, setReply] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');

  if (!state) return <Navigate to="/interview" replace />;

  const submit = async () => {
    setLoading(true);
    setError('');
    try {
      const res = await api.post('interview/answer/', { interview_id: state.interview_id, answer });
      setReply(res.data);
    } catch (err) {
      setError(err.response?.data?.detail || 'Could not submit your answer.');
    } finally {
      setLoading(false);
    }
  };

  const goNext = () => {
    if (reply.finished) {
      navigate(`/interview/result/${reply.result_id}`);
      return;
    }
    setCurrent({ number: reply.number, total: reply.total, question: reply.question });
    setAnswer('');
    setReply(null);
  };

  const ev = reply?.evaluation;

  return (
    <div className="a-page">
      <h1>Mock Interview</h1>
      <div className="a-card">
        <div className="a-top"><span>Question {current.number}/{current.total}</span></div>
        <div className="a-track">
          <div className="a-fill" style={{ width: `${(current.number / current.total) * 100}%` }} />
        </div>
        <h3 className="a-q">{current.question}</h3>
        <textarea
          className="a-ta"
          rows={6}
          placeholder="Type your answer here..."
          value={answer}
          onChange={(e) => setAnswer(e.target.value)}
          disabled={!!reply}
        />
        {!reply && (
          <div className="a-nav">
            <span />
            <button className="a-btn" onClick={submit} disabled={loading || !answer.trim()}>
              {loading ? 'Evaluating...' : 'Submit Answer'}
            </button>
          </div>
        )}
        {ev && (
          <div className="a-fb">
            <p className="a-label">Score</p>
            <p className="a-big">{ev.score}/10</p>
            <div className="a-grid">
              <div className="a-box"><span>Technical</span><strong>{ev.technical}/10</strong></div>
              <div className="a-box"><span>Communication</span><strong>{ev.communication}/10</strong></div>
              <div className="a-box"><span>Accuracy</span><strong>{ev.accuracy}/10</strong></div>
            </div>
            <p style={{ marginTop: 12 }}><strong>Feedback:</strong> {ev.feedback}</p>
            <div className="a-nav">
              <span />
              <button className="a-btn" onClick={goNext}>
                {reply.finished ? 'View Result' : 'Next Question'}
              </button>
            </div>
          </div>
        )}
        {error && <p className="a-err">{error}</p>}
      </div>
    </div>
  );
}