import { StrictMode } from "react";
import { createRoot } from "react-dom/client";
import { BrowserRouter as Router, Routes, Route } from "react-router-dom";
import { Landing } from "./screens/Landing";
import { Editor } from "./screens/Editor";

createRoot(document.getElementById("app") as HTMLElement).render(
  <StrictMode>
    <Router>
      <Routes>
        <Route path="/" element={<Landing />} />
        <Route path="/editor" element={<Editor />} />
      </Routes>
    </Router>
  </StrictMode>
);