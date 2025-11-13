from utils.video_exporter import export_video_from_frames
from PIL import Image
import tempfile
import os

# 1️⃣ Create dummy frames
frames = []
for i, color in enumerate(["red", "green", "blue"]):
    img = Image.new("RGB", (640, 360), color=color)
    path = tempfile.NamedTemporaryFile(delete=False, suffix=".png").name
    img.save(path)
    frames.append(path)

# 2️⃣ No audio for now
video_path = export_video_from_frames(frames, audio_path=None, fps=1)

print("✅ Video exported to:", video_path)
print("Check outputs/videos/ for the result.")

# Clean up temp frames (optional)
for f in frames:
    os.remove(f)
