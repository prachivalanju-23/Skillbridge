import { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import api from '../../api/axios';
import '../../components/shared.css';
import './resume.css';

export default function ResumeUploadPage() {
  const [file, setFile] = useState(null);
  const [error, setError] = useState('');
  const [loading, setLoading] = useState(false);
  const navigate = useNavigate();

  const submit = async () => {
    if (!file) return setError('Please choose a PDF or DOCX file');
    setLoading(true);
    setError('');
    try {
      const form = new FormData();
      form.append('resume', file);
      await api.post('resume/upload/', form);
      navigate('/resume-analysis');
    } catch (e) {
      setError((e.response && e.response.data && e.response.data.message) || 'Upload failed');
    }
    setLoading(false);
  };

  return (
    <div className="rs-page">
      <div className="rs-hero">
        <div>
          <h2>Upload Your Resume</h2>
          <p>We find your skills, score your resume and build your student profile.</p>
          <div className="rs-steps">
            <span className="rs-step">1 · Upload</span>
            <span className="rs-step">2 · Analyze</span>
            <span className="rs-step">3 · Skill gap</span>
          </div>
        </div>
      </div>

      <div className="sb-card rs-blue">
        <label className="rs-drop">
          <div className="rs-drop-ico">📄</div>
          <b>{file ? file.name : 'Click to choose your resume'}</b>
          <span>PDF or DOCX, max 5 MB</span>
          <input type="file" accept=".pdf,.docx" hidden onChange={(e) => setFile(e.target.files[0])} />
        </label>
        {error && <p className="sb-error">{error}</p>}
        <div className="rs-actions">
          <button className="sb-btn" onClick={submit} disabled={loading}>
            {loading ? 'Analyzing...' : 'Upload & Analyze'}
          </button>
        </div>
      </div>
    </div>
  );
}