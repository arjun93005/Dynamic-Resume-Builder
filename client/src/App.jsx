import React from "react";
import UploadHero from "./components/UploadHero";
import Sidebar from "./components/Sidebar";

export default function App() {
  // global state could go here later
  return (
    <div className="app min-h-screen bg-[#0f1216] text-white flex">
      <aside className="sidebar w-64 bg-[#0b0e12] border-r border-white/5">
        <Sidebar />
      </aside>

      <main className="main flex-1 p-6">
        <div className="hero max-w-3xl mx-auto">
          <h1 className="text-3xl font-semibold">Dynamic Resume Analyzer</h1>
          <p className="text-white/70 mt-2">
            Upload a resume to extract sections, scores and get feedback instantly.
          </p>

          {/* Upload + result card */}
          <UploadHero />
        </div>
      </main>
    </div>
  );
}
