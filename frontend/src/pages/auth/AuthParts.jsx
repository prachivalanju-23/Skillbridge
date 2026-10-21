import { useState } from 'react';
import './auth.css';
import Logo from '../../components/Logo';

export function apiError(e, fallback) {
  const d = e.response && e.response.data;
  if (!d || typeof d === 'string') return fallback;
  if (d.message) return d.message;
  if (d.detail) return d.detail;
  const v = Object.values(d)[0];
  return Array.isArray(v) ? v[0] : String(v);
}

export function strength(pw) {
  let s = 0;
  if (pw.length >= 8) s++;
  if (/[a-z]/.test(pw) && /[A-Z]/.test(pw)) s++;
  if (/\d/.test(pw)) s++;
  if (/[^A-Za-z0-9]/.test(pw)) s++;
  return s;
}

export function AuthShell({ title, subtitle, children, footer }) {
  return (
    <div className="au-wrap">
      <div className="au-side">
        <div className="au-brand"><Logo size={50} light /></div>
        <h1>Build the skills.<br />Land the career.</h1>
        <p>An AI-powered career and skill development platform for students.</p>
        <ul className="au-points">
          <li><span>📄</span> Analyze your resume with AI</li>
          <li><span>🎯</span> Find your skill gaps</li>
          <li><span>🗺️</span> Get a personal learning roadmap</li>
          <li><span>💼</span> Match with the right jobs</li>
          <li><span>🎤</span> Practice mock interviews</li>
        </ul>
      </div>

      <div className="au-main">
        <div className="au-card">
          <div className="au-card-logo"><Logo size={40} /></div>
          <h2>{title}</h2>
          <p className="au-sub">{subtitle}</p>
          {children}
          {footer && <div className="au-foot">{footer}</div>}
        </div>
      </div>
    </div>
  );
}

export function Field({ label, ...props }) {
  return (
    <label className="au-field">
      <span>{label}</span>
      <input {...props} />
    </label>
  );
}

export function PasswordField({ label, meter, ...props }) {
  const [show, setShow] = useState(false);
  const s = meter ? strength(props.value || '') : 0;
  const names = ['Too weak', 'Weak', 'Fair', 'Good', 'Strong'];
  return (
    <label className="au-field">
      <span>{label}</span>
      <div className="au-pass">
        <input type={show ? 'text' : 'password'} {...props} />
        <button type="button" className="au-eye" onClick={() => setShow(!show)}>
          {show ? 'Hide' : 'Show'}
        </button>
      </div>
      {meter && props.value && (
        <div className="au-meter">
          <div className="au-meter-bar"><div className={`au-lvl-${s}`} style={{ width: `${s * 25}%` }} /></div>
          <small>{names[s]}</small>
        </div>
      )}
    </label>
  );
}