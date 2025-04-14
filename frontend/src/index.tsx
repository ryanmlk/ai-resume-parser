import { createRoot } from "react-dom/client";
import { BrowserRouter as Router, Routes, Route } from "react-router-dom";
import { Landing } from "./screens/Landing";
import { Editor } from "./screens/Editor";
import { Login } from "./screens/Login";
import { SignUp } from "./screens/SignUp";
import { AuthProvider } from "./auth/AuthContext";
import ProtectedRoute from "./auth/ProtectedRoute";

createRoot(document.getElementById("app") as HTMLElement).render(
  <Router>
    <AuthProvider>
      <Routes>
        {/* Protect the Landing page */}
        <Route
          path="/"
          element={
            <ProtectedRoute>
              <Landing />
            </ProtectedRoute>
          }
        />
        <Route path="/editor" element={<Editor />} />
        <Route path="/login" element={<Login />} />
        <Route path="/signUp" element={<SignUp />} />
      </Routes>
    </AuthProvider>
  </Router>
);