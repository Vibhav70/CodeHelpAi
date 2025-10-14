import React from "react";
import {
  BrowserRouter as Router,
  Routes,
  Route,
  Navigate,
} from "react-router-dom";
import { AuthProvider, useAuth } from "./contexts/AuthContext";
import Navbar from "./components/Navbar";
import LoginPage from "./pages/LoginPage";
import DashboardPage from "./pages/DashboardPage"; // 1. Import the new dashboard page
import ProjectChatPage from "./pages/ProjectChatPage";
import DocumentationPage from "./pages/DocumentationPage";
import AdminPage from "./pages/AdminPage";

// A wrapper for routes that require authentication
const PrivateRoute = ({ children }) => {
  const { isAuthenticated } = useAuth();
  return isAuthenticated ? children : <Navigate to="/login" />;
};

function App() {
  return (
    <AuthProvider>
      <Router>
        <div className="flex flex-col min-h-screen bg-gray-50">
          <Navbar />
          <main className="flex-grow">
            <Routes>
              <Route path="/login" element={<LoginPage />} />
              <Route
                path="/"
                element={
                  <PrivateRoute>
                    {/* 2. Use the new DashboardPage here */}
                    <DashboardPage />
                  </PrivateRoute>
                }
              />
              <Route
                path="/projects/:projectId"
                element={
                  <PrivateRoute>
                    <ProjectChatPage />
                  </PrivateRoute>
                }
              />

              <Route
                path="/admin"
                element={
                  <PrivateRoute>
                    <AdminPage/>
                  </PrivateRoute>
                }
              />

              {/* You can add more routes here later */}
              <Route
                path="/project/:projectId/docs"
                element={
                  <PrivateRoute>
                    <DocumentationPage />
                  </PrivateRoute>
                }
              />
            </Routes>
          </main>
        </div>
      </Router>
    </AuthProvider>
  );
}

export default App;
