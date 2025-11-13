# backend/app/tts_api.py
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from pathlib import Path
import uuid
import os

from .tts_engine import (
    synthesize_text_to_wav,
    get_audio_duration_ms,
    concat_wav_files_ordered
)

router = APIRouter()

# Output folder
AUDIO_DIR = Path(__file__).resolve().parents[2] / "outputs" / "audio"
AUDIO_DIR.mkdir(parents=True, exist_ok=True)


class TTSRequest(BaseModel):
    lines: list[str]   # narration per step
    voice_rate: int = 170


@router.post("/tts")
def generate_tts(req: TTSRequest):
    if not req.lines:
        raise HTTPException(status_code=400, detail="No narration lines provided")

    temp_files = []
    timestamps = []
    cursor = 0

    # 1️⃣ Create WAV for each line
    for line in req.lines:
        wav_path = synthesize_text_to_wav(line, rate=req.voice_rate)
        duration = get_audio_duration_ms(wav_path)

        timestamps.append({
            "start_ms": cursor,
            "end_ms": cursor + duration,
            "duration_ms": duration,
            "text": line
        })
        cursor += duration

        temp_files.append(wav_path)

    # 2️⃣ Combine into final narration file
    out_name = f"tts_{uuid.uuid4().hex}.wav"
    out_path = AUDIO_DIR / out_name
    total_ms = concat_wav_files_ordered(temp_files, str(out_path))

    # 3️⃣ Cleanup temp files
    for f in temp_files:
        try: os.remove(f)
        except: pass

    return {
        "ok": True,
        "audio_file": str(out_path),
        "total_ms": total_ms,
        "timestamps": timestamps
    }
