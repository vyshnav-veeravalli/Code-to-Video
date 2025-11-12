# backend/app/api.py
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Any
from utils.ast_parser import parse_code_to_scene
from utils.scene_generator import generate_scene_with_trace

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