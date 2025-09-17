import React, { createContext, useState, useContext, useEffect } from 'react';
import { loginUser } from '../api/apiClient';
// --- THIS IS THE FIX ---
// We use a named import { jwtDecode } instead of a default import.
import { jwtDecode } from 'jwt-decode';

const AuthContext = createContext(null);

export const AuthProvider = ({ children }) => {
  const [user, setUser] = useState(null);
  const [token, setToken] = useState(localStorage.getItem('authToken') || null);

  useEffect(() => {
    if (token) {
      try {
        // Use the correctly imported function name
        const decoded = jwtDecode(token);
        
        // Optional: Check if the token is expired
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
      return true;
    } catch (error) {
      console.error("Login failed:", error);
      return false;
    }
  };

  const logout = () => {
    setUser(null);
    setToken(null);
    localStorage.removeItem('authToken');
  };

  const authValue = {
    user,
    token,
    login,
    logout,
    isAuthenticated: !!token,
  };

  return <AuthContext.Provider value={authValue}>{children}</AuthContext.Provider>;
};

export const useAuth = () => {
  return useContext(AuthContext);
};

