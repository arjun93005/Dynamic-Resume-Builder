import React, { useState } from "react";

export default function UploadHero(){
  const [file, setFile] = useState(null);
  const [loading, setLoading] = useState(false);
  const [result, setResult] = useState(null);
  const [error, setError] = useState("");

  const onFileChange = (e) => {
    setError("");
    setResult(null);
    setFile(e.target.files?.[0] ?? null);
  };

  const upload = async () => {
    if (!file) { setError("Please select a file to upload."); return; }
    setLoading(true);
    setError("");
    try {
      const fd = new FormData();
      fd.append("file", file);
      const res = await fetch("/api/resume/analyze", {
        method: "POST",
        body: fd,
      });
      const json = await res.json();
      if (!res.ok) throw new Error(json.error || json.message || "Upload failed");
      setResult(json);
    } catch (err) {
      setError(err.message || String(err));
    } finally {
      setLoading(false);
    }
  };

  return (
    <div>
      <div className="upload-row">
        <input className="file-input" type="file" onChange={onFileChange} />
        <button className="btn" onClick={upload} disabled={loading}>
          {loading ? "Analyzing..." : "Upload & Analyze"}
        </button>
      </div>

      {error && <div className="error">{error}</div>}

      {result && (
        <div className="result-box">
          <div><strong>Report ID:</strong> {result.reportId}</div>
          <div className="small">Checksum: {result.checksum}</div>
          <div style={{marginTop:8}}>
            <button className="btn" onClick={() => window.open(`/api/resume/result/${result.reportId}`)}>
              View JSON
            </button>
          </div>
        </div>
      )}
    </div>
  );
}
