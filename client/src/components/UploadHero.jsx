// client/src/components/UploadHero.jsx
import React, { useState } from "react";

export default function UploadHero({ onJson }) {
  const [file, setFile] = useState(null);
  const [uploading, setUploading] = useState(false);
  const [error, setError] = useState("");
  const [errorDetails, setErrorDetails] = useState("");

  const onPick = (e) => {
    setError("");
    setErrorDetails("");
    const f = e.target.files?.[0];
    setFile(f || null);
  };

  const onUpload = async () => {
    if (!file) return;
    setUploading(true);
    setError("");
    setErrorDetails("");

    try {
      const form = new FormData();
      form.append("file", file);
      const res = await fetch("http://127.0.0.1:5000/api/resume/analyze", {
        method: "POST",
        body: form,
      });

      if (res.status === 422) {
        const data = await res.json();
        setError(data.error || "Corrupted or unreadable file");
        setErrorDetails(data.details || "");
        return;
      }

      if (!res.ok) {
        const msg = await res.text();
        throw new Error(msg || `Upload failed (${res.status})`);
      }

      const data = await res.json();
      onJson(data);
    } catch (e) {
      setError(e.message || "Upload failed");
    } finally {
      setUploading(false);
    }
  };

  const onRetry = () => {
    setError("");
    setErrorDetails("");
    setFile(null);
  };

  return (
    <div className="upload-row">
      <label className="file-input">
        <input
          type="file"
          className="hidden"
          onChange={onPick}
          accept=".pdf,.doc,.docx,.txt"
        />
        {file ? file.name : "Choose File..."}
      </label>
      <button
        onClick={onUpload}
        disabled={!file || uploading}
        className="btn"
      >
        {uploading ? "Analyzing..." : "Upload & Analyze"}
      </button>

      {/* ⚠️ Error Banner */}
      {error && (
        <div className="error-banner" style={{ marginTop: "16px" }}>
          <p><strong>{error}</strong></p>
          {errorDetails && <p className="text-sm mt-1">{errorDetails}</p>}
          <button
            onClick={onRetry}
            className="mt-2 px-3 py-1.5 text-xs bg-gray-800 text-white rounded hover:bg-gray-700"
          >
            Try Again
          </button>
        </div>
      )}
    </div>
  );
}
