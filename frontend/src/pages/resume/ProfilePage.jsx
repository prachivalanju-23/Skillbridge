import { useEffect, useState } from 'react';
import { Link } from 'react-router-dom';
import api from '../../api/axios';
import '../../components/shared.css';
import './resume.css';
import { Ring, Head, initials } from './ui';

export default function ProfilePage() {
  const [d, setD] = useState(null);
  const [empty, setEmpty] = useState(false);

  useEffect(() => {
    api.get('resume/profile/')
      .then((r) => setD(r.data))
      .catch((e) => { if (e.response && e.response.status === 404) setEmpty(true); });
  }, []);

  if (empty) return <div className="rs-page">No profile yet. <Link to="/resume-upload">Upload your resume</Link></div>;
  if (!d) return <div className="rs-page">Loading...</div>;

  const gap = d.skill_gap;

  return (
    <div className="rs-page">
      <div className="rs-hero">
        <div className="rs-who">
          <div className="rs-avatar">{initials(d.name)}</div>
          <div>
            <h2>{d.name || 'Student Profile'}</h2>
            <p>Student Profile Dashboard</p>
            {d.email && <p>✉ {d.email}</p>}
          </div>
        </div>
        <Ring value={d.resume_score} label="Resume score" />
      </div>

      <div className="rs-grid">
        <div className="sb-card rs-indigo">
          <div className="rs-tile-ico">🎯</div>
          <div>
            <h4>Target Role</h4>
            <h3>{d.target_role || 'Not selected'}</h3>
          </div>
        </div>
        <div className="sb-card rs-green">
          {gap ? <Ring value={gap.percentage} suffix="%" small light /> : <div className="rs-tile-ico">📈</div>}
          <div>
            <h4>Skill Match</h4>
            <div className="rs-big">{gap ? `${gap.percentage}%` : '--'}</div>
          </div>
        </div>
        <div className="sb-card rs-rose">
          <div className="rs-tile-ico">🧩</div>
          <div>
            <h4>Missing Skills</h4>
            <div className="rs-big">{gap ? gap.missing.length : '--'}</div>
          </div>
        </div>
      </div>

      <div className="sb-card rs-blue">
        <Head icon="🧠" title="Current Skills" extra={d.skills.length} />
        <div className="rs-tags">
          {d.skills.map((s) => <span key={s} className="rs-tag rs-ok">{s}</span>)}
        </div>
      </div>

      <div className="sb-card rs-rose">
        <Head icon="🧩" title="Missing Skills" extra={gap ? gap.missing.length : undefined} />
        {gap ? (
          gap.missing.length
            ? <div className="rs-tags">{gap.missing.map((s) => <span key={s} className="rs-tag rs-miss">{s}</span>)}</div>
            : <p>No missing skills for this role. 🎉</p>
        ) : (
          <p>Choose a target role in <Link to="/skill-gap">Skill Gap</Link> to see your missing skills.</p>
        )}
      </div>

      <div className="rs-actions">
        <Link className="sb-btn" to="/resume-upload">Upload new resume</Link>
        <Link className="sb-btn sb-btn-ghost" to="/skill-gap">Change target role</Link>
      </div>
    </div>
  );
}