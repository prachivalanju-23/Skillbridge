import { useState } from 'react';
import { Link, Navigate, useNavigate } from 'react-router-dom';
import { useAuth } from '../../context/AuthContext';
import { AuthShell, Field, PasswordField, apiError } from './AuthParts';

export default function LoginPage() {
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [error, setError] = useState('');
  const [loading, setLoading] = useState(false);
  const { login, isLoggedIn } = useAuth();
  const navigate = useNavigate();

  if (isLoggedIn) return <Navigate to="/" replace />;

  const submit = async (e) => {
    e.preventDefault();
    setError('');
    setLoading(true);
    try {
      await login(email, password);
      navigate('/');
    } catch (err) {
      if (err.response && err.response.status === 401) setError('Invalid email or password');
      else setError(apiError(err, 'Could not reach the server. Is the backend running?'));
    }
    setLoading(false);
  };

  return (
    <AuthShell
      title="Welcome back 👋"
      subtitle="Log in to continue your career journey."
      footer={<>New to SkillBridge? <Link className="au-link" to="/register">Create an account</Link></>}
    >
      <form onSubmit={submit}>
        {error && <div className="au-error">{error}</div>}
        <Field label="Email" type="email" placeholder="you@example.com" autoComplete="email"
               value={email} onChange={(e) => setEmail(e.target.value)} required />
        <PasswordField label="Password" placeholder="Enter your password" autoComplete="current-password"
                       value={password} onChange={(e) => setPassword(e.target.value)} required />
        <div className="au-row"><Link className="au-link" to="/forgot-password">Forgot password?</Link></div>
        <button className="au-btn" type="submit" disabled={loading}>{loading ? 'Logging in...' : 'Log in'}</button>
      </form>
    </AuthShell>
  );
}