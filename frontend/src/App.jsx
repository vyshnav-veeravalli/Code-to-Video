import React from "react";
import Editor from "./components/Editor";
import CanvasPlayer from "./components/CanvasPlayer";
import TimelineControls from "./components/TimeLineControls";

export default function App() {
  return (
    <div style={{ display: "flex", height: "100vh", background: "#0f0f0f", color: "white" }}>
      <div style={{ flex: 0.4, padding: "20px" }}>
        <Editor />
        <TimelineControls />
      </div>

      <div style={{ flex: 0.6, padding: "20px" }}>
        <CanvasPlayer />
      </div>
    </div>
  );
}
