import { create } from "zustand";
import { generateSceneRuntime, requestTTS, exportVideo } from "../api/backend";

export const useSceneStore = create((set, get) => ({
  // ---------------------------
  // STATE
  // ---------------------------
  code: "x = 10\nprint(x)",

  runtimeScene: [],
  currentFrame: 0,
  isPlaying: false,
  fps: 2, // slow for debugging (later set to 24)

  audio: null, // { audio_file, total_ms, timestamps }

  canvasDims: { width: 1280, height: 720 },

  // ---------------------------
  // ACTIONS
  // ---------------------------

  setCode: (code) => set({ code }),

  loadRuntimeScene: async () => {
    const code = get().code;
    const scene = await generateSceneRuntime(code);
    set({
      runtimeScene: scene,
      currentFrame: 0,
      isPlaying: false,
    });
  },

  nextFrame: () => {
    const { currentFrame, runtimeScene } = get();
    if (currentFrame < runtimeScene.length - 1) {
      set({ currentFrame: currentFrame + 1 });
    } else {
      set({ isPlaying: false });
    }
  },

  prevFrame: () => {
    const { currentFrame } = get();
    if (currentFrame > 0) {
      set({ currentFrame: currentFrame - 1 });
    }
  },

  play: () => set({ isPlaying: true }),
  pause: () => set({ isPlaying: false }),
  reset: () => set({ currentFrame: 0, isPlaying: false }),

  // ---------------------------
  // AUDIO
  // ---------------------------

  generateNarration: async () => {
    const { runtimeScene } = get();
    const lines = runtimeScene.map((step) => {
      if (step.type === "assign")
        return `Assign operation: ${step.code}`;
      if (step.type === "print")
        return `Print statement output ${step.output}`;
      if (step.type.includes("loop"))
        return `Loop iteration at line ${step.lineno}`;
      return `Executing line ${step.lineno}`;
    });

    const audio = await requestTTS(lines);
    set({ audio });
  },

  // ---------------------------
  // EXPORT VIDEO
  // ---------------------------

  exportVideo: async (frames) => {
    const { audio } = get();
    const fps = 24;

    const res = await exportVideo(frames, audio?.audio_file || null, fps);
    return res.video_path;
  },
}));
