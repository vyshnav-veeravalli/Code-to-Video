import React, { useEffect } from "react";
import { useSceneStore } from "../state/useSceneStore";

export default function TimelineControls() {
  const {
    currentFrame,
    runtimeScene,
    isPlaying,
    play,
    pause,
    nextFrame,
    prevFrame,
    reset,
    fps,
  } = useSceneStore();

  // Auto-play effect
  useEffect(() => {
    if (!isPlaying) return;

    const interval = setInterval(() => {
      nextFrame();
    }, 1000 / fps);

    return () => clearInterval(interval);
  }, [isPlaying, fps, nextFrame]);

  return (
    <div style={{ display: "flex", gap: "10px", marginTop: "20px" }}>
      <button onClick={prevFrame}>◀ Prev</button>

      {!isPlaying ? (
        <button onClick={play}>▶ Play</button>
      ) : (
        <button onClick={pause}>⏸ Pause</button>
      )}

      <button onClick={nextFrame}>Next ▶</button>
      <button onClick={reset}>⟲ Reset</button>

      <span style={{ marginLeft: "10px" }}>
        Frame: {currentFrame + 1} / {runtimeScene.length}
      </span>
    </div>
  );
}
