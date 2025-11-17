import axios from "axios";

const API_BASE = "http://localhost:8000/api";

export async function generateSceneStatic(code) {
  try {
    const res = await axios.post(`${API_BASE}/generate-scene`, { code });
    return res.data.scene;
  } catch (err) {
    console.error("Static AST error:", err);
    throw err;
  }
}

export async function generateSceneRuntime(code) {
  try {
    const res = await axios.post(`${API_BASE}/generate-scene-runtime`, { code });
    return res.data.scene;
  } catch (err) {
    console.error("Runtime scene error:", err);  
    throw err;
  }
}

export async function requestTTS(lines) {
  try {
    const res = await axios.post(`${API_BASE}/tts`, { lines });
    return res.data;
  } catch (err) {
    console.error("TTS error:", err);
    throw err;
  }
}

export async function exportVideo(frames, audioPath, fps = 24) {
  try {
    const res = await axios.post(`${API_BASE}/export-video`, {
      frames,
      audio_path: audioPath,
      fps
    });
    return res.data;
  } catch (err) {
    console.error("Video export error:", err);
    throw err;
  }
}
