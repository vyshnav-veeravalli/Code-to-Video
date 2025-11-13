# backend/app/api.py
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Any, List, Optional
from utils.ast_parser import parse_code_to_scene
from utils.scene_generator import generate_scene_with_trace
from utils.video_exporter import export_video_from_frames


router = APIRouter()

class CodeRequest(BaseModel):
    code: str

@router.post("/generate-scene")
def generate_scene(req: CodeRequest):
    try:
        scene = parse_code_to_scene(req.code)
        return {"ok": True, "scene": scene}
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/generate-scene-runtime")
def generate_scene_runtime(req: CodeRequest):
    """Dynamic runtime scene with locals and outputs"""
    try:
        scene = generate_scene_with_trace(req.code)
        return {"ok": True, "scene": scene}
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    


# ----------------------------------------------------------
#  🆕  Export video endpoint
# ----------------------------------------------------------

class ExportVideoRequest(BaseModel):
    frames: List[str]
    audio_path: Optional[str] = None
    fps: int = 24


@router.post("/export-video")
def export_video(req: ExportVideoRequest):
    """
    Combine frames + audio into final MP4.
    Returns the saved video path.
    """
    try:
        video_path = export_video_from_frames(req.frames, req.audio_path, req.fps)
        return {"ok": True, "video_path": video_path}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))