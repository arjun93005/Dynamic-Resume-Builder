import React, { useState } from "react";

export default function UploadHero({ onJson }) {
  const [file, setFile] = useState(null);
  const [reportId, setReportId] = useState("");
  const [jsonData, setJsonData] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");

  const handleFile = (e) => {
    setFile(e.target.files[0]);
    setError("");
    setJsonData(null);
  };

  const handleUpload = async () => {
    if (!file) return;
    setLoading(true);
    setError("");
    try {
      const form = new FormData();
      form.append("file", file);
      const res = await fetch("http://127.0.0.1:5000/api/resume/analyze", {
        method: "POST",
        body: form,
      });
      const data = await res.json();
      setReportId(data.reportId);
      await fetchJson(data.reportId);
    } catch {
      setError("Upload failed.");
    } finally {
      setLoading(false);
    }
  };

  const fetchJson = async (id) => {
  try {
    const res = await fetch(`http://127.0.0.1:5000/api/resume/result/${id}`);
    const data = await res.json();
    // 🔹 make sure the frontend receives same structure
    if (onJson) onJson(data);
  } catch {
    setError("Error fetching analysis.");
  }
};

  return (
    <div>
      <div className="upload-row">
        <input
          type="file"
          className="file-input"
          accept=".pdf,.doc,.docx,.txt"
          onChange={handleFile}
        />
        <button onClick={handleUpload} disabled={loading} className="btn">
          {loading ? "Analyzing..." : "Upload & Analyze"}
        </button>
      </div>
      {error && <div style={{ color: "red", marginTop: 8 }}>{error}</div>}
    </div>
  );
}

