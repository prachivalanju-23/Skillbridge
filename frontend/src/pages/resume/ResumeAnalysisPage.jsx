import { useEffect, useState } from 'react';
import { Link } from 'react-router-dom';
import api from '../../api/axios';
import '../../components/shared.css';
import './resume.css';
import { Ring, Head, initials } from './ui';

const MAX = { skills: 40, education: 15, projects: 15, certifications: 10, experience: 10, contact: 10 };
const LABEL = { skills: 'Skills', education: 'Education', projects: 'Projects',
  certifications: 'Certifications', experience: 'Experience', contact: 'Contact info' };

function Section({ icon, title, items, tint }) {
  return (
    <div className={`sb-card ${tint}`}>
      <Head icon={icon} title={title} />
      {items && items.length ? (
        <ul className="rs-list">{items.map((i, k) => <li key={k}>{i}</li>)}</ul>
      ) : (
        <p>Not found in your resume</p>
      )}
    </div>
  );
}

export default function ResumeAnalysisPage() {
  const [d, setD] = useState(null);
  const [empty, setEmpty] = useState(false);

  useEffect(() => {
    api.get('resume/profile/')
      .then((r) => setD(r.data))
      .catch((e) => { if (e.response && e.response.status === 404) setEmpty(true); });
  }, []);

  if (empty) return <div className="rs-page">No resume yet. <Link to="/resume-upload">Upload one</Link></div>;
  if (!d) return <div className="rs-page">Loading...</div>;

  const brk = d.score_breakdown || {};

  return (
    <div className="rs-page">
      <div className="rs-hero">
        <div className="rs-who">
          <div className="rs-avatar">{initials(d.name)}</div>
          <div>
            <h2>{d.name || 'Resume Analysis'}</h2>
            {d.email && <p>✉ {d.email}</p>}
            {d.phone && <p>📞 {d.phone}</p>}
          </div>
        </div>
        <Ring value={d.resume_score} label="Resume score" />
      </div>

      <div className="sb-card rs-blue">
        <Head icon="🧠" title="Skills Identified" extra={d.skills.length} />
        <div className="rs-tags">
          {d.skills.map((s) => <span key={s} className="rs-tag">{s}</span>)}
        </div>
      </div>

      <div className="sb-card rs-slate">
        <Head icon="📊" title="Score Breakdown" />
        {Object.keys(MAX).map((k) => (
          <div className="rs-brk" key={k}>
            <span>{LABEL[k]}</span>
            <div className="rs-bar"><div style={{ width: `${((brk[k] || 0) / MAX[k]) * 100}%` }} /></div>
            <span>{brk[k] || 0}/{MAX[k]}</span>
          </div>
        ))}
      </div>

      <Section icon="🎓" title="Education" items={d.education} tint="rs-indigo" />
      <Section icon="🚀" title="Projects" items={d.projects} tint="rs-cyan" />
      <Section icon="📜" title="Certifications" items={d.certifications} tint="rs-sky" />
      <Section icon="💼" title="Experience" items={d.experience} tint="rs-blue" />

      <div className="rs-actions">
        <Link className="sb-btn" to="/skill-gap">Check Skill Gap</Link>
        <Link className="sb-btn sb-btn-ghost" to="/profile">Go to Profile</Link>
      </div>
    </div>
  );
}