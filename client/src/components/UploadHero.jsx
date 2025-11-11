import React, { useState } from "react";

export default function UploadHero() {
  const [file, setFile] = useState(null);
  const [reportId, setReportId] = useState("");
  const [checksum, setChecksum] = useState("");
  const [jsonData, setJsonData] = useState(null);
  const [uploading, setUploading] = useState(false);
  const [error, setError] = useState("");
  const [errorDetails, setErrorDetails] = useState("");

  const onPick = async (e) => {
    const f = e.target.files?.[0];
    resetAll();
    setFile(f || null);

    if (f) {
      const buf = await f.arrayBuffer();
      const digest = await crypto.subtle.digest("SHA-256", buf);
      const bytes = Array.from(new Uint8Array(digest));
      const hex = bytes.map((b) => b.toString(16).padStart(2, "0")).join("");
      setChecksum(hex);
    }
  };

  const onUpload = async () => {
    if (!file) return;
    setUploading(true);
    setError("");
    setErrorDetails("");
    setJsonData(null);
    setReportId("");

    try {
      const form = new FormData();
      form.append("file", file);

      const res = await fetch("http://127.0.0.1:5000/api/resume/analyze", {
        method: "POST",
        body: form,
      });

      // ✅ Handle backend status codes
      if (res.status === 422) {
        const data = await res.json();
        setError(data.error || "Corrupted or unreadable file");
        setErrorDetails(data.details || "");
        return;
      }
      if (!res.ok) {
        const msg = await safeText(res);
        throw new Error(msg || `Upload failed (${res.status})`);
      }

      const data = await res.json();
      setReportId(data.reportId || "");
      setJsonData(data);
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
    setChecksum("");
    setReportId("");
    setJsonData(null);
  };

  const resetAll = () => {
    setJsonData(null);
    setReportId("");
    setChecksum("");
    setError("");
    setErrorDetails("");
  };

  return (
    <div className="mt-6">
      <div className="rounded-2xl bg-white border border-gray-200 p-6 shadow-xl transition-all duration-200">
        {/* Upload row */}
        <div className="flex items-center gap-3">
          <label className="inline-flex items-center px-3 py-2 rounded-md bg-gray-100 border border-gray-300 hover:border-gray-400 cursor-pointer text-gray-700">
            <input
              type="file"
              className="hidden"
              onChange={onPick}
              accept=".pdf,.doc,.docx,.txt"
            />
            <span className="text-sm font-medium">Browse…</span>
          </label>

          <div className="flex-1 truncate text-sm text-gray-600">
            {file ? file.name : "No file selected"}
          </div>

          <button
            onClick={onUpload}
            disabled={!file || uploading}
            className="px-4 py-2 rounded-md bg-orange-500 hover:bg-orange-600 disabled:opacity-50 text-sm font-medium text-white transition-transform duration-150 hover:-translate-y-0.5"
          >
            {uploading ? "Analyzing…" : "Upload & Analyze"}
          </button>
        </div>

        {/* ⚠️ Error Banner for Corrupted/Empty Files */}
        {error && (
          <div className="error-banner mt-4">
            <p className="font-semibold">{error}</p>
            {errorDetails && (
              <p className="text-sm mt-1 opacity-80">{errorDetails}</p>
            )}
            <button
              onClick={onRetry}
              className="mt-2 px-3 py-1.5 text-xs bg-gray-800 text-white rounded hover:bg-gray-700 transition-all"
            >
              Try Again
            </button>
          </div>
        )}

        {/* Normal result data if success */}
        {jsonData && reportId && (
          <div className="mt-4 rounded-xl bg-gray-50 border border-gray-200 p-4 text-sm text-gray-700">
            ✅ Analysis Completed for <b>{jsonData.filename}</b>
            <pre className="mt-2 max-h-72 overflow-auto bg-gray-100 rounded-xl p-3 text-xs">
              {JSON.stringify(jsonData.sections, null, 2)}
            </pre>
          </div>
        )}
      </div>
    </div>
  );
}

async function safeText(res) {
  try {
    return await res.text();
  } catch {
    return "";
  }
}