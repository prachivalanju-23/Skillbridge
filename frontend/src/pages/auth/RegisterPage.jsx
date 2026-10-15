import { useState } from 'react';
import { useNavigate, Link } from 'react-router-dom';
import { useAuth } from '../../context/AuthContext';
import '../../components/shared.css';

export default function RegisterPage() {
  const [name, setName] = useState('');
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [error, setError] = useState('');
  const { register } = useAuth();
  const navigate = useNavigate();

  const submit = async () => {
    setError('');
    try {
      await register(name, email, password);
      navigate('/login');
    } catch (e) {
      const data = e.response && e.response.data;
      setError((data && (data.email || data.password)) ? JSON.stringify(data) : 'Registration failed');
    }
  };

  return (
    <div className="sb-form sb-card">
      <h2>Register</h2>
      <input placeholder="Full name" value={name} onChange={(e) => setName(e.target.value)} />
      <input placeholder="Email" value={email} onChange={(e) => setEmail(e.target.value)} />
      <input type="password" placeholder="Password" value={password} onChange={(e) => setPassword(e.target.value)} />
      {error && <p className="sb-error">{error}</p>}
      <button className="sb-btn" onClick={submit}>Register</button>
      <p>Already registered? <Link to="/login">Login</Link></p>
    </div>
  );
}