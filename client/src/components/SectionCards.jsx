// client/src/components/SectionCards.jsx
import React from "react";

export default function SectionCards({ section, json }) {
  if (!json) return <div className="placeholder">Upload a resume to view extracted details.</div>;

  const data = json.sections || {};

  const renderContact = () => {
    const c = data.contact_info || {};
    return (
      <div className="json-view">
        <p><strong>Email:</strong> {c.email || "—"}</p>
        <p><strong>Phone:</strong> {c.phone || "—"}</p>
        <p><strong>LinkedIn:</strong> {c.linkedin || "—"}</p>
        <p><strong>GitHub:</strong> {c.github || "—"}</p>
      </div>
    );
  };

  const renderEducation = () => (
    <div className="json-view">{data.education || "—"}</div>
  );

  const renderExperience = () => (
    <div className="json-view">{data.experience || "—"}</div>
  );

  const renderProjects = () => (
    <div className="json-view">Project extraction coming soon.</div>
  );

  const renderCertifications = () => (
    <div className="json-view">Certification extraction coming soon.</div>
  );

  const renderSkills = () => {
    const s = data.skills || [];
    return (
      <ul className="skills-list">
        {s.length > 0
          ? s.map((skill, i) => <li key={i}>{skill}</li>)
          : <li>—</li>}
      </ul>
    );
  };

  switch (section) {
    case "contact": return renderContact();
    case "education": return renderEducation();
    case "experience": return renderExperience();
    case "projects": return renderProjects();
    case "certifications": return renderCertifications();
    case "skills": return renderSkills();
    default: return <div className="placeholder">Select a section to view data.</div>;
  }
}
