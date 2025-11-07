import React, { useState } from "react";
import UploadHero from "./components/UploadHero";
import Sidebar from "./components/Sidebar";

export default function App(){
  // global state could go here later
  return (
    <div className="app">
      <aside className="sidebar">
        <Sidebar />
      </aside>

      <main className="main">
        <div className="hero">
          <h1>Dynamic Resume Analyzer</h1>
          <p>Upload a resume to extract sections, scores and get feedback instantly.</p>
          <UploadHero />
        </div>
      </main>
    </div>
  );
}
