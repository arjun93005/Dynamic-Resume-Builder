// client/src/App.jsx
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

          {/* Upload Component */}
          <UploadHero onJson={(d) => setJsonData(d)} />

          {/* Only show cards after analysis */}
          {jsonData && (
            <>
              {/* Score + Recommendations */}
              <div className="cards">
                {/* ✅ Resume Score */}
                <div className="card">
                  <h3>Resume Quality Score</h3>
                  <p className="text-4xl font-bold text-orange-600 mt-2">
                    {jsonData.score?.score ?? "—"}/100
                  </p>
                  {jsonData.score?.notes?.length > 0 && (
                    <ul className="list-disc list-inside text-sm mt-3 text-gray-600">
                      {jsonData.score.notes.slice(0, 2).map((n, i) => (
                        <li key={i}>{n}</li>
                      ))}
                    </ul>
                  )}
                </div>

                {/* Recommendations placeholder */}
                <div className="card placeholder-card">
                  Recommendations (coming soon)
                </div>
              </div>

              {/* File Metadata */}
              <div className="meta-card">
                <div className="meta-grid">
                  <div>
                    <h3>File Metadata</h3>
                    <p><strong>Filename:</strong> {jsonData.metadata?.filename}</p>
                    <p><strong>Status:</strong> {jsonData.status || "done"}</p>
                  </div>
                  <div>
                    <p><strong>File Type:</strong> {jsonData.metadata?.file_type}</p>
                    <p><strong>Word Count:</strong> {jsonData.metadata?.word_count}</p>
                    <p><strong>Character Count:</strong> {jsonData.metadata?.character_count}</p>
                  </div>
                </div>

                {/* ⚠️ Missing Sections */}
                {jsonData.missing_sections?.length > 0 && (
                  <div className="missing-banner mt-3">
                    ⚠️ <strong>Missing sections detected:</strong>{" "}
                    {jsonData.missing_sections.join(", ")}
                  </div>
                )}
              </div>

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

              {/* Section Data */}
              <div className="section-content">
                <SectionCards section={activeSection} json={jsonData} />
              </div>
            </>
          )}

          {!jsonData && (
            <div className="placeholder">
              Upload a resume to begin analysis.
            </div>
          )}
        </div>
      </div>
    </div>
  );
}
