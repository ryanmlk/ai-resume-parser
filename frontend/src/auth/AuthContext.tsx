import React, { createContext, useState, useEffect, ReactNode } from "react";
import { useNavigate } from "react-router-dom";

interface AuthContextType {
  isAuthenticated: boolean;
  login: (token: string) => void;
  logout: () => void;
}

export const AuthContext = createContext<AuthContextType | null>(null);

export const AuthProvider = ({ children }: { children: ReactNode }) => {
  const [isAuthenticated, setIsAuthenticated] = useState<boolean>(false);
  const navigate = useNavigate();

  useEffect(() => {
    try {
      // Check if token exists in localStorage
      const token = localStorage.getItem("access_token");
      if (token) {
        setIsAuthenticated(true);
      }
    } catch (error) {
      console.error("Error initializing AuthContext:", error);
    }
  }, []);

  const login = (token: string) => {
    try {
      localStorage.setItem("access_token", token);
      setIsAuthenticated(true);
      navigate("/dashboard"); // Redirect to a protected route
    } catch (error) {
      console.error("Error during login:", error);
    }
  };

  const logout = () => {
    try {
      localStorage.removeItem("access_token");
      setIsAuthenticated(false);
      navigate("/login"); // Redirect to login page
    } catch (error) {
      console.error("Error during logout:", error);
    }
  };

  return (
    <AuthContext.Provider value={{ isAuthenticated, login, logout }}>
      {children}
    </AuthContext.Provider>
  );
};