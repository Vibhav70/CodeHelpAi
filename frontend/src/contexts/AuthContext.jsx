import React, { createContext, useState, useContext, useEffect } from 'react';
import { loginUser } from '../api/apiClient';
import { jwtDecode } from 'jwt-decode';

const AuthContext = createContext(null);

export const AuthProvider = ({ children }) => {
  const [user, setUser] = useState(null);
  const [token, setToken] = useState(localStorage.getItem('authToken') || null);
  const [role, setRole] = useState(localStorage.getItem('userRole') || 'user');

  useEffect(() => {
    if (token) {
      try {
        const decoded = jwtDecode(token);

        const isExpired = decoded.exp * 1000 < Date.now();
        if (isExpired) {
          console.log("Token expired, logging out.");
          logout();
          return;
        }

        setUser({ username: decoded.sub });
        localStorage.setItem('authToken', token);
      } catch (error) {
        console.error("Invalid token:", error);
        logout();
      }
    } else {
      localStorage.removeItem('authToken');
    }
  }, [token]);

  const login = async (username, password) => {
    try {
      const response = await loginUser(username, password);
      setToken(response.data.access_token);

      // ✅ Hardcode admin detection for now
      const isAdmin = username === 'admin' && password === 'admin';
      const userRole = isAdmin ? 'admin' : 'user';

      setRole(userRole);
      localStorage.setItem('userRole', userRole);

      return true;
    } catch (error) {
      console.error("Login failed:", error);
      return false;
    }
  };

  const logout = () => {
    setUser(null);
    setToken(null);
    setRole('user');
    localStorage.removeItem('authToken');
    localStorage.removeItem('userRole');
  };

  const authValue = {
    user,
    token,
    role,
    login,
    logout,
    isAuthenticated: !!token,
  };

  return <AuthContext.Provider value={authValue}>{children}</AuthContext.Provider>;
};

export const useAuth = () => {
  return useContext(AuthContext);
};
