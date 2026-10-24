import { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import api from '../../api/axios';
import '../assessment.css';

const CATEGORIES = ['All', 'Logical', 'Quantitative', 'Verbal', 'Technical'];
const LETTERS = ['A', 'B', 'C', 'D'];

export default function AptitudeTestPage() {
  const navigate = useNavigate();
  const [category, setCategory] = useState('All');
  const [questions, setQuestions] = useState([]);
  const [answers, setAnswers] = useState({});
  const [current, setCurrent] = useState(0);
  const [started, setStarted] = useState(false);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');

  const startTest = async () => {
    setLoading(true);
    setError('');
    try {
      const params = category === 'All' ? {} : { category };
      const res = await api.get('aptitude/questions/', { params });
      setQuestions(res.data);
      setAnswers({});
      setCurrent(0);
      setStarted(true);
    } catch {
      setError('Could not load questions. Is the backend running?');
    } finally {
      setLoading(false);
    }
  };

  const submitTest = async () => {
    setLoading(true);
    setError('');
    try {
      const payload = questions.map((q) => ({ question_id: q.id, selected_index: answers[q.id] }));
      const res = await api.post('aptitude/submit/', { answers: payload });
      navigate('/aptitude/result', { state: { result: res.data } });
    } catch {
      setError('Could not submit the test. Please try again.');
      setLoading(false);
    }
  };

  if (!started) {
    return (
      <div className="a-page">
        <h1>Aptitude Assessment</h1>
        <p>Choose a category and test yourself.</p>
        <div className="a-row">
          <select className="a-select" value={category} onChange={(e) => setCategory(e.target.value)}>
            {CATEGORIES.map((c) => (
              <option key={c} value={c}>{c === 'All' ? 'All categories (20 questions)' : c}</option>
            ))}
          </select>
          <button className="a-btn" onClick={startTest} disabled={loading}>
            {loading ? 'Loading...' : 'Start Test'}
          </button>
        </div>
        {error && <p className="a-err">{error}</p>}
      </div>
    );
  }

  const q = questions[current];
  const answered = Object.keys(answers).length;
  const isLast = current === questions.length - 1;

  return (
    <div className="a-page">
      <h1>Aptitude Assessment</h1>
      <div className="a-card">
        <div className="a-top">
          <span>Question {current + 1}/{questions.length}</span>
          <span className="a-tag">{q.category}</span>
        </div>
        <div className="a-track">
          <div className="a-fill" style={{ width: `${((current + 1) / questions.length) * 100}%` }} />
        </div>
        <h3 className="a-q">{q.text}</h3>
        <div className="a-options">
          {q.options.map((opt, i) => (
            <button
              key={i}
              className={`a-opt ${answers[q.id] === i ? 'sel' : ''}`}
              onClick={() => setAnswers({ ...answers, [q.id]: i })}
            >
              <strong>{LETTERS[i]})</strong> {opt}
            </button>
          ))}
        </div>
        <div className="a-nav">
          <button className="a-btn a-btn2" onClick={() => setCurrent(current - 1)} disabled={current === 0}>
            Previous
          </button>
          {isLast ? (
            <button className="a-btn" onClick={submitTest} disabled={loading || answered < questions.length}>
              {loading ? 'Submitting...' : 'Submit Test'}
            </button>
          ) : (
            <button className="a-btn" onClick={() => setCurrent(current + 1)}>Next</button>
          )}
        </div>
        <p className="a-muted">
          Answered {answered} of {questions.length}
          {isLast && answered < questions.length && ' (answer all questions to submit)'}
        </p>
        {error && <p className="a-err">{error}</p>}
      </div>
    </div>
  );
}