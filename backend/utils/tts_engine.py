# backend/app/utils/tts_engine.py
import pyttsx3
import tempfile
import os
from pydub import AudioSegment

def synthesize_text_to_wav(text: str, rate: int = 170, voice_id: str = None) -> str:
    """
    Convert plain text to a WAV file using offline TTS (pyttsx3).
    Returns path to the generated WAV file.
    """
    if not text.strip():
        raise ValueError("Empty text input for TTS")

    engine = pyttsx3.init()
    engine.setProperty('rate', rate)

    # Select voice (optional)
    voices = engine.getProperty('voices')
    if voice_id:
        try:
            engine.setProperty('voice', voice_id)
        except Exception:
            pass
    else:
        # Default to first English voice
        for v in voices:
            if "english" in v.name.lower():
                engine.setProperty('voice', v.id)
                break

    # Create temp WAV file
    tmp_file = tempfile.NamedTemporaryFile(delete=False, suffix=".wav")
    tmp_file.close()

    engine.save_to_file(text, tmp_file.name)
    engine.runAndWait()

    return tmp_file.name


def get_audio_duration_ms(wav_path: str) -> int:
    """Return duration (ms) of a WAV file"""
    audio = AudioSegment.from_wav(wav_path)
    return len(audio)


def concat_wav_files_ordered(file_paths, out_path: str) -> int:
    """Concatenate multiple WAV files into one and return total duration."""
    combined = None
    for path in file_paths:
        seg = AudioSegment.from_wav(path)
        if combined is None:
            combined = seg
        else:
            combined += seg

    combined.export(out_path, format="wav")
    return len(combined)
