import { useState } from 'react';
import { Link, useNavigate, useParams } from 'react-router-dom';
import api from '../../api/axios';
import { AuthShell, PasswordField, apiError } from './AuthParts';

export default function ResetPasswordPage() {
  const { uid, token } = useParams();
  const [password, setPassword] = useState('');
  const [confirm, setConfirm] = useState('');
  const [error, setError] = useState('');
  const [done, setDone] = useState(false);
  const [loading, setLoading] = useState(false);
  const navigate = useNavigate();

  const submit = async (e) => {
    e.preventDefault();
    setError('');
    if (password !== confirm) return setError('Passwords do not match');
    setLoading(true);
    try {
      await api.post('auth/reset-password/', { uid, token, password });
      setDone(true);
      setTimeout(() => navigate('/login'), 2500);
    } catch (err) {
      setError(apiError(err, 'Could not reset the password.'));
    }
    setLoading(false);
  };

  return (
    <AuthShell
      title="Set a new password 🔒"
      subtitle="Choose a strong password for your account."
      footer={<Link className="au-link" to="/login">← Back to login</Link>}
    >
      {done ? (
        <div className="au-ok">
          <div className="au-big">✅</div>
          Your password was changed. Taking you to the login page...
        </div>
      ) : (
        <form onSubmit={submit}>
          {error && (
            <div className="au-error">
              {error} {error.includes('invalid or has expired') && <Link className="au-link" to="/forgot-password">Request a new link</Link>}
            </div>
          )}
          <PasswordField label="New password" meter placeholder="At least 8 characters" autoComplete="new-password"
                         value={password} onChange={(e) => setPassword(e.target.value)} required />
          <PasswordField label="Confirm new password" placeholder="Type it again" autoComplete="new-password"
                         value={confirm} onChange={(e) => setConfirm(e.target.value)} required />
          <button className="au-btn" type="submit" disabled={loading}>
            {loading ? 'Saving...' : 'Change password'}
          </button>
        </form>
      )}
    </AuthShell>
  );
}