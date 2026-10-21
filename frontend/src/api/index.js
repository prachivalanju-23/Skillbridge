import api from './axios';

// Translates the old page calls (/jobs, /jobs/match, /roadmaps/career/1)
// to the Django URLs (jobs/, jobs/, roadmap/career/1/)
function fix(url) {
  let u = url.replace(/^\/+/, '');
  u = u.replace(/^jobs\/match/, 'jobs');
  u = u.replace(/^roadmaps\//, 'roadmap/');
  if (!u.endsWith('/')) u += '/';
  return u;
}

export default {
  get: (url, config) => api.get(fix(url), config),
  post: (url, data, config) => api.post(fix(url), data, config),
};