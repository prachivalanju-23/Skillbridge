import { createContext, useContext, useState } from 'react';
import api from '../api/axios';

const AuthContext = createContext();
export const useAuth = () => useContext(AuthContext);

export function AuthProvider({ children }) {
  const [isLoggedIn, setIsLoggedIn] = useState(!!localStorage.getItem('access'));

  const login = async (email, password) => {
    const res = await api.post('auth/login/', { username: email.trim().toLowerCase(), password });
    localStorage.setItem('access', res.data.access);
    localStorage.setItem('refresh', res.data.refresh);
    setIsLoggedIn(true);
  };

  const register = async (name, email, password) => {
    await api.post('auth/register/', { first_name: name, email: email.trim().toLowerCase(), password });
    await login(email, password);
  };

  const logout = () => {
    localStorage.removeItem('access');
    localStorage.removeItem('refresh');
    setIsLoggedIn(false);
  };

  return (
    <AuthContext.Provider value={{ isLoggedIn, login, register, logout }}>
      {children}
    </AuthContext.Provider>
  );
}