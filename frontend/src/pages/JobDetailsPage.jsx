import { useEffect, useState } from 'react';
import { Link, useParams, useSearchParams } from 'react-router-dom';
import api from '../api';
import './details.css';

export default function JobDetailsPage() {
  const { id } = useParams();
  const [searchParams] = useSearchParams();
  const skills = searchParams.get('skills') || '';

  const [job, setJob] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');

  useEffect(() => {
    setLoading(true);
    setError('');

    api
      .get(`/jobs/${id}`, { params: skills ? { skills } : {} })
      .then((res) => setJob(res.data))
      .catch((err) =>
        setError(
          err.response?.status === 404
            ? 'Job not found.'
            : 'Could not load this job. Is the backend running?'
        )
      )
      .finally(() => setLoading(false));
  }, [id, skills]);

  const backLink = skills ? `/jobs?skills=${encodeURIComponent(skills)}` : '/jobs';
  const hasMatch = job && job.matchPercent !== undefined;

  const badgeClass = (percent) => {
    if (percent >= 70) return 'match-badge high';
    if (percent >= 40) return 'match-badge medium';
    return 'match-badge low';
  };

  return (
    <div className="page">
      <Link className="back-link" to={backLink}>
        ← Back to jobs
      </Link>

      {loading && <p className="message">Loading job...</p>}
      {error && <p className="message error">{error}</p>}

      {job && (
        <div className="details-card">
          {hasMatch && (
            <span className={badgeClass(job.matchPercent)}>
              {job.matchPercent}% match
            </span>
          )}

          <h1>{job.title}</h1>
          <p className="company">{job.company}</p>
          <p className="meta">
            {job.location} • {job.jobType} • {job.experienceLevel} •{' '}
            {job.careerCategory}
          </p>

          <div className="details-section">
            <h3>About the role</h3>
            <p>{job.description || 'No description available.'}</p>
          </div>

          <div className="details-section">
            <h3>Required skills</h3>
            <div className="skills">
              {job.requiredSkills.map((skill) => {
                let tagClass = 'skill-tag';
                if (hasMatch) {
                  tagClass += job.matchedSkills.includes(skill)
                    ? ' matched'
                    : ' missing';
                }
                return (
                  <span className={tagClass} key={skill}>
                    {skill}
                  </span>
                );
              })}
            </div>
          </div>

          {hasMatch ? (
            <div className="details-section">
              <h3>Your skill gap</h3>
              {job.missingSkills.length === 0 ? (
                <p>You have all the required skills for this job. 🎉</p>
              ) : (
                <>
                  <p>Skills you still need to learn for this job:</p>
                  <ul className="gap-list">
                    {job.missingSkills.map((skill) => (
                      <li key={skill}>{skill}</li>
                    ))}
                  </ul>
                </>
              )}
            </div>
          ) : (
            <p className="message">
              Enter your skills on the Jobs page to see your match and skill gap
              for this job.
            </p>
          )}

          {job.applyLink && (
            <a
              className="apply-btn"
              href={job.applyLink}
              target="_blank"
              rel="noreferrer"
            >
              Apply now
            </a>
          )}
        </div>
      )}
    </div>
  );
}