import { useEffect, useState } from 'react';
import { Link } from 'react-router-dom';
import api from '../../api/axios';
import '../../components/shared.css';
import './resume.css';
import { Ring, Head } from './ui';

export default function SkillGapPage() {
  const [roles, setRoles] = useState([]);
  const [roleId, setRoleId] = useState('');
  const [result, setResult] = useState(null);
  const [error, setError] = useState('');

  useEffect(() => {
    api.get('resume/roles/').then((r) => setRoles(r.data));
  }, []);

  const compare = async () => {
    setError('');
    try {
      const r = await api.post('resume/skill-gap/', { career_id: Number(roleId) });
      setResult(r.data);
    } catch (e) {
      setError((e.response && e.response.data && e.response.data.message) || 'Something went wrong');
    }
  };

  return (
    <div className="rs-page">
      <div className="rs-hero">
        <div>
          <h2>Skill Gap Detection</h2>
          <p>Pick a target role and see which skills you have and which are missing.</p>
        </div>
        <div className="rs-avatar">🎯</div>
      </div>

      <div className="sb-card rs-blue">
        <Head icon="🎯" title="Choose your target role" />
        <select value={roleId} onChange={(e) => setRoleId(e.target.value)}>
          <option value="">-- Select a role --</option>
          {roles.map((r) => <option key={r.id} value={r.id}>{r.title}</option>)}
        </select>
        <div className="rs-actions">
          <button className="sb-btn" onClick={compare} disabled={!roleId}>Compare</button>
        </div>
        {error && (
          <p className="sb-error">{error} <Link to="/resume-upload">Upload resume</Link></p>
        )}
      </div>

      {result && (
        <>
          <div className="sb-card rs-green">
            <div className="rs-result-top">
              <Ring value={result.percentage} suffix="%" label="match" small light />
              <div>
                <h3>{result.target_role}</h3>
                <p>You have {result.matched.length} of {result.required.length} required skills.</p>
              </div>
            </div>
            <table className="rs-table">
              <thead><tr><th>Skill</th><th>Status</th></tr></thead>
              <tbody>
                {result.required.map((s) => (
                  <tr key={s}>
                    <td>{s}</td>
                    <td>
                      {result.matched.includes(s)
                        ? <span className="rs-pill rs-pill-ok">✓ Have</span>
                        : <span className="rs-pill rs-pill-no">✗ Missing</span>}
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>

          <div className="sb-card rs-rose">
            <Head icon="🧩" title="Skill Gap" extra={result.missing.length} />
            {result.missing.length ? (
              <div className="rs-tags">
                {result.missing.map((s) => <span key={s} className="rs-tag rs-miss">{s}</span>)}
              </div>
            ) : (
              <p>You have all the skills for this role. 🎉</p>
            )}
            <div className="rs-actions">
              <Link className="sb-btn" to="/profile">View Profile Dashboard</Link>
            </div>
          </div>
        </>
      )}
    </div>
  );
}