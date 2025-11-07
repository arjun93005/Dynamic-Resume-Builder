import React, { useState } from "react";

/**
 * UploadHero: keeps your original visual layout, but adds:
 * - file picker + "Upload & Analyze"
 * - client-side SHA-256 checksum
 * - POST /api/resume/analyze -> { reportId }
 * - "View JSON" to GET /api/resume/result/:id and show data
 *
 * Tailwind classes are used for quick styling similar to your screenshot.
 */
export default function UploadHero() {
  const [file, setFile] = useState(null);
  const [reportId, setReportId] = useState("");
  const [checksum, setChecksum] = useState("");
  const [jsonData, setJsonData] = useState(null);
  const [uploading, setUploading] = useState(false);
  const [error, setError] = useState("");

  const onPick = async (e) => {
    const f = e.target.files?.[0];
    setJsonData(null);
    setReportId("");
    setChecksum("");
    setError("");
    setFile(f || null);

    if (f) {
      // Compute SHA-256 checksum to mirror your UI
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
    setJsonData(null);
    setReportId("");

    try {
      const form = new FormData();
      form.append("file", file);

      // Use your Flask route that the tests use
      const res = await fetch("http://127.0.0.1:5000/api/resume/analyze", {
        method: "POST",
        body: form,
      });

      if (!res.ok) {
        const msg = await safeText(res);
        throw new Error(msg || `Upload failed (${res.status})`);
      }

      const data = await res.json();
      setReportId(data.reportId || "");
    } catch (e) {
      setError(e.message || "Upload failed");
    } finally {
      setUploading(false);
    }
  };

  const onViewJson = async () => {
    if (!reportId) return;
    try {
      const res = await fetch(
        `http://127.0.0.1:5000/api/resume/result/${encodeURIComponent(reportId)}`
      );
      const data = await res.json();
      setJsonData(data);
    } catch {
      setJsonData({ error: "Failed to fetch JSON" });
    }
  };

  return (
    <div className="mt-6">
      <div className="rounded-2xl bg-[#12161c] border border-white/10 p-5 shadow-xl">
        {/* File row */}
        <div className="flex items-center gap-3">
          <label
            className="inline-flex items-center px-3 py-2 rounded-md bg-[#0b0e12] border border-white/10 hover:border-white/20 cursor-pointer"
            title="Browse"
          >
            <input
              type="file"
              className="hidden"
              onChange={onPick}
              accept=".pdf,.doc,.docx,.txt"
            />
            <span className="text-sm">Browse…</span>
          </label>

          <div className="flex-1 truncate text-sm text-white/80">
            {file ? file.name : "No file selected"}
          </div>

          <button
            onClick={onUpload}
            disabled={!file || uploading}
            className="px-4 py-2 rounded-md bg-green-600 hover:bg-green-500 disabled:opacity-50 text-sm font-medium"
          >
            {uploading ? "Uploading…" : "Upload & Analyze"}
          </button>
        </div>

        {/* Result block */}
        {(reportId || checksum || error) && (
          <div className="mt-4 rounded-xl bg-black/40 p-4">
            {error ? (
              <p className="text-red-400 text-sm">{error}</p>
            ) : (
              <>
                {reportId && (
                  <p className="text-sm">
                    <span className="text-white/60">Report ID:</span>{" "}
                    <span className="font-mono">{reportId}</span>
                  </p>
                )}
                {checksum && (
                  <p className="text-sm mt-1">
                    <span className="text-white/60">Checksum:</span>{" "}
                    <span className="font-mono break-all">{checksum}</span>
                  </p>
                )}

                <div className="mt-3">
                  <button
                    onClick={onViewJson}
                    disabled={!reportId}
                    className="px-3 py-1.5 rounded-md bg-green-700 hover:bg-green-600 disabled:opacity-50 text-sm"
                  >
                    View JSON
                  </button>
                </div>
              </>
            )}
          </div>
        )}

        {/* JSON viewer */}
        {jsonData && (
          <pre className="mt-4 max-h-72 overflow-auto rounded-xl bg-[#0b0e12] border border-white/10 p-3 text-xs">
{JSON.stringify(jsonData, null, 2)}
          </pre>
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
