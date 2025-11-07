import React from "react";

export default function Sidebar(){
  return (
    <>
      <div className="brand">
        <div className="logo">DRA</div>
        <div>
          <h2>Dynamic Resume Analyzer</h2>
          <div style={{fontSize:12, color:"#99a0a6"}}>Think Less. Do More.</div>
        </div>
      </div>

      <div className="menu">
        <button>🏁 Dashboard</button>
        <button>📁 Upload</button>
        <button>📊 Reports</button>
        <button>⚙️ Settings</button>
        <button>🧾 Docs</button>
      </div>

      
    </>
  );
}
