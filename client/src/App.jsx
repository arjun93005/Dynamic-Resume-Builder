import React, { useState } from "react";
import UploadHero from "./components/UploadHero";
import SectionCards from "./components/SectionCards";
import "./index.css";

export default function App() {
  const [jsonData, setJsonData] = useState(null);
  const [activeSection, setActiveSection] = useState("contact");

  const sections = ["contact", "education", "experience", "projects", "certifications", "skills"];

  return (
    <div className="app">
      <div className="container">
        <div className="hero">
          <h1>Dynamic Resume Analyzer</h1>
          <p>Upload a resume to extract key information and view details by section.</p>

          <UploadHero onJson={(d) => setJsonData(d)} />

          {/* Score & Recommendations placeholders */}
          <div className="cards">
            <div className="card placeholder-card">Score (coming soon)</div>
            <div className="card placeholder-card">Recommendations (coming soon)</div>
          </div>

          {/* File Metadata */}
          {jsonData && (
            <div className="meta-card">
              <div className="meta-grid">
                <div>
                  <h3>File Metadata</h3>
                  <p><strong>Filename:</strong> {jsonData.filename || "—"}</p>
                  <p><strong>Status:</strong> {jsonData.status || "done"}</p>
                </div>
                <div>
                  <p><strong>File Type:</strong> {getFileType(jsonData.filename)}</p>
                  <p><strong>Word Count:</strong> {countWords(jsonData.sections)}</p>
                  <p><strong>Character Count:</strong> {countChars(jsonData.sections)}</p>
                </div>
              </div>
            </div>
          )}

          {/* Section Tabs */}
          <div className="tabs">
            {sections.map((tab) => (
              <div
                key={tab}
                className={`tab ${activeSection === tab ? "active" : ""}`}
                onClick={() => setActiveSection(tab)}
              >
                {tab.charAt(0).toUpperCase() + tab.slice(1)}
              </div>
            ))}
          </div>

          {/* Section Content */}
          <div className="section-content">
            <SectionCards section={activeSection} json={jsonData} />
          </div>
        </div>
      </div>
    </div>
  );
}

// Helper utilities
function getFileType(filename = "") {
  if (!filename) return "—";
  const ext = filename.split(".").pop().toUpperCase();
  return ext || "—";
}

function countWords(sections) {
  if (!sections) return 0;
  const text = Object.values(sections).join(" ");
  return text.trim().split(/\s+/).length;
}

function countChars(sections) {
  if (!sections) return 0;
  const text = Object.values(sections).join(" ");
  return text.length;
}
