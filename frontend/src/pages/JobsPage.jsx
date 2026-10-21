import { useEffect, useState } from 'react';
import { Link, useSearchParams } from 'react-router-dom';
import api from '../api';

export default function JobsPage() {
  const [searchParams] = useSearchParams();
  const initialSkills = searchParams.get('skills') || '';
  const initialCategory = searchParams.get('category') || 'All';

  const [jobs, setJobs] = useState([]);
  const [category, setCategory] = useState(initialCategory);
  const [skillsInput, setSkillsInput] = useState(initialSkills);
  const [appliedSkills, setAppliedSkills] = useState(initialSkills);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');

  useEffect(() => {
    setLoading(true);
    setError('');

    const request = appliedSkills
      ? api.get('/jobs/match', { params: { skills: appliedSkills } })
      : api.get('/jobs');

    request
      .then((res) => setJobs(res.data))
      .catch(() => setError('Could not load jobs. Is the backend running?'))
      .finally(() => setLoading(false));
  }, [appliedSkills]);

  const handleSubmit = (e) => {
    e.preventDefault();
    setAppliedSkills(skillsInput.trim());
  };

  const categories = ['All', ...new Set(jobs.map((j) => j.careerCategory))];
  const visibleJobs =
    category === 'All' ? jobs : jobs.filter((j) => j.careerCategory === category);

  const badgeClass = (percent) => {
    if (percent >= 70) return 'match-badge high';
    if (percent >= 40) return 'match-badge medium';
    return 'match-badge low';
  };

  const detailsLink = (id) =>
    appliedSkills
      ? `/jobs/${id}?skills=${encodeURIComponent(appliedSkills)}`
      : `/jobs/${id}`;

  return (
    <div className="page">
      <h1>Job Recommendations</h1>
      <p className="message">
        Enter your skills (separated by commas) to see how well you match each job.
      </p>

      <form className="search-bar" onSubmit={handleSubmit}>
        <input
          type="text"
          placeholder="e.g. React, JavaScript, HTML, CSS, Git"
          value={skillsInput}
          onChange={(e) => setSkillsInput(e.target.value)}
        />
        <button type="submit">Find matches</button>
      </form>

      <div className="toolbar">
        <label htmlFor="category">Career category:</label>
        <select
          id="category"
          value={category}
          onChange={(e) => setCategory(e.target.value)}
        >
          {categories.map((c) => (
            <option key={c} value={c}>
              {c}
            </option>
          ))}
        </select>
      </div>

      {loading && <p className="message">Loading jobs...</p>}
      {error && <p className="message error">{error}</p>}

      <div className="job-grid">
        {visibleJobs.map((job) => {
          const hasMatch = job.matchPercent !== undefined;

          return (
            <Link className="job-card-link" to={detailsLink(job._id)} key={job._id}>
              <div className="job-card">
                {hasMatch && (
                  <span className={badgeClass(job.matchPercent)}>
                    {job.matchPercent}% match
                  </span>
                )}
                <h3>{job.title}</h3>
                <p className="company">{job.company}</p>
                <p className="meta">
                  {job.location} • {job.jobType} • {job.experienceLevel}
                </p>
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
            </Link>
          );
        })}
      </div>
    </div>
  );
}