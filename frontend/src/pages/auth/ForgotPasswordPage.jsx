import { useState } from 'react';
import { Link } from 'react-router-dom';
import api from '../../api/axios';
import { AuthShell, Field, apiError } from './AuthParts';

export default function ForgotPasswordPage() {
  const [email, setEmail] = useState('');
  const [sent, setSent] = useState(false);
  const [error, setError] = useState('');
  const [loading, setLoading] = useState(false);

  const submit = async (e) => {
    e.preventDefault();
    setError('');
    setLoading(true);
    try {
      await api.post('auth/forgot-password/', { email });
      setSent(true);
    } catch (err) {
      setError(apiError(err, 'Something went wrong. Please try again.'));
    }
    setLoading(false);
  };

  return (
    <AuthShell
      title="Forgot password? 🔑"
      subtitle="Enter your email and we will send you a reset link."
      footer={<Link className="au-link" to="/login">← Back to login</Link>}
    >
      {sent ? (
        <div className="au-ok">
          If <b>{email}</b> is registered, a reset link is on its way. It works for 1 hour.
          Check your inbox (and spam folder).
        </div>
      ) : (
        <form onSubmit={submit}>
          {error && <div className="au-error">{error}</div>}
          <Field label="Email" type="email" placeholder="you@example.com" autoComplete="email"
                 value={email} onChange={(e) => setEmail(e.target.value)} required />
          <button className="au-btn" type="submit" disabled={loading}>
            {loading ? 'Sending...' : 'Send reset link'}
          </button>
        </form>
      )}
    </AuthShell>
  );
}