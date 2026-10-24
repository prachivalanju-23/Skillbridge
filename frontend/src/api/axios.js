import axios from 'axios';

const BASE = 'http://localhost:8000/api/';
const api = axios.create({ baseURL: BASE });

function logoutAndRedirect() {
  localStorage.removeItem('access');
  localStorage.removeItem('refresh');
  if (window.location.pathname !== '/login') window.location.href = '/login';
}

api.interceptors.request.use((config) => {
  const token = localStorage.getItem('access');
  if (token) config.headers.Authorization = `Bearer ${token}`;
  return config;
});

let refreshing = null;

api.interceptors.response.use(
  (res) => res,
  async (err) => {
    const original = err.config;
    const status = err.response && err.response.status;
    const isAuthCall = original && original.url && original.url.includes('auth/');

    if (status === 401 && original && !isAuthCall) {
      const refresh = localStorage.getItem('refresh');
      if (refresh && !original._retry) {
        original._retry = true;
        try {
          if (!refreshing) refreshing = axios.post(BASE + 'auth/refresh/', { refresh });
          const res = await refreshing;
          localStorage.setItem('access', res.data.access);
          original.headers.Authorization = 'Bearer ' + res.data.access;
          return api(original);
        } catch (e) {
          logoutAndRedirect();
          return Promise.reject(e);
        } finally {
          refreshing = null;
        }
      }
      logoutAndRedirect();
    }
    return Promise.reject(err);
  }
);

export default api;