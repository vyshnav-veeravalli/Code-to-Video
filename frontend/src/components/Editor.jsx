import React from "react";
import { useSceneStore } from "../state/useSceneStore";

export default function Editor() {
  const code = useSceneStore((s) => s.code);
  const setCode = useSceneStore((s) => s.setCode);
  const loadRuntimeScene = useSceneStore((s) => s.loadRuntimeScene);
  const reset = useSceneStore((s) => s.reset);

  const handleGenerate = async () => {
    await loadRuntimeScene();
    reset(); // set frameIndex to 0
  };

  return (
    <div
      style={{
        width: "100%",
        background: "#1a1a1a",
        padding: "16px",
        borderRadius: "8px",
        display: "flex",
        flexDirection: "column",
        gap: "10px",
      }}
    >
      <h2 style={{ margin: 0 }}>Code Editor</h2>

      <textarea
        value={code}
        onChange={(e) => setCode(e.target.value)}
        style={{
          width: "100%",
          height: "250px",
          fontFamily: "monospace",
          fontSize: "15px",
          background: "#111",
          color: "white",
          padding: "10px",
          borderRadius: "6px",
          border: "1px solid #444",
        }}
      />

      <button
        onClick={handleGenerate}
        style={{
          padding: "10px 14px",
          width: "fit-content",
          background: "#4f46e5",
          borderRadius: "6px",
          color: "white",
          border: "none",
          cursor: "pointer",
        }}
      >
        Generate Animation
      </button>
    </div>
  );
}
