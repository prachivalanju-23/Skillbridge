import { useState } from 'react';
import { Link, Navigate, useNavigate } from 'react-router-dom';
import { useAuth } from '../../context/AuthContext';
import { AuthShell, Field, PasswordField, apiError } from './AuthParts';

export default function RegisterPage() {
  const [name, setName] = useState('');
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [confirm, setConfirm] = useState('');
  const [error, setError] = useState('');
  const [loading, setLoading] = useState(false);
  const { register, isLoggedIn } = useAuth();
  const navigate = useNavigate();

  if (isLoggedIn) return <Navigate to="/" replace />;

  const submit = async (e) => {
    e.preventDefault();
    setError('');
    if (password !== confirm) return setError('Passwords do not match');
    setLoading(true);
    try {
      await register(name, email, password);
      navigate('/resume-upload');
    } catch (err) {
      setError(apiError(err, 'Registration failed. Is the backend running?'));
    }
    setLoading(false);
  };

  return (
    <AuthShell
      title="Create your account 🚀"
      subtitle="Join SkillBridge and plan your career."
      footer={<>Already have an account? <Link className="au-link" to="/login">Log in</Link></>}
    >
      <form onSubmit={submit}>
        {error && <div className="au-error">{error}</div>}
        <Field label="Full name" placeholder="Your name" autoComplete="name"
               value={name} onChange={(e) => setName(e.target.value)} required />
        <Field label="Email" type="email" placeholder="you@example.com" autoComplete="email"
               value={email} onChange={(e) => setEmail(e.target.value)} required />
        <PasswordField label="Password" meter placeholder="At least 8 characters" autoComplete="new-password"
                       value={password} onChange={(e) => setPassword(e.target.value)} required />
        <PasswordField label="Confirm password" placeholder="Type the password again" autoComplete="new-password"
                       value={confirm} onChange={(e) => setConfirm(e.target.value)} required />
        <button className="au-btn" type="submit" disabled={loading}>{loading ? 'Creating account...' : 'Create account'}</button>
      </form>
    </AuthShell>
  );
}