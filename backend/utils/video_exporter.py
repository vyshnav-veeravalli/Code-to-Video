# backend/app/utils/video_exporter.py
import os
import uuid
from pathlib import Path
from moviepy.editor import ImageSequenceClip, AudioFileClip

OUTPUT_DIR = Path(__file__).resolve().parents[2] / "outputs" / "videos"
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)


def export_video_from_frames(frame_paths, audio_path=None, fps=24):
    """
    Combine a list of frame image paths + optional audio into a final MP4 video.
    Returns the output video path.
    """

    if not frame_paths:
        raise ValueError("No frames provided for video export.")

    # Create video from image sequence
    clip = ImageSequenceClip(frame_paths, fps=fps)

    # Attach audio if provided
    if audio_path and os.path.exists(audio_path):
        audio_clip = AudioFileClip(audio_path)
        clip = clip.set_audio(audio_clip)

    # Output file path
    out_name = f"video_{uuid.uuid4().hex}.mp4"
    out_path = OUTPUT_DIR / out_name

    # Export the video
    clip.write_videofile(
        str(out_path),
        codec="libx264",
        audio_codec="aac",
        verbose=False,
        logger=None
    )

    return str(out_path)
