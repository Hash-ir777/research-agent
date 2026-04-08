from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from app.agents.research_agent import generate_full_paper
from app.agents.parser import parse_file
import os

router = APIRouter(prefix="/generate", tags=["generate"])

UPLOAD_DIR = "uploads"

class GenerateRequest(BaseModel):
    content_filename: str
    template: str = "IEEE"

@router.post("/paper")
async def generate_paper(request: GenerateRequest):
    file_path = f"{UPLOAD_DIR}/{request.content_filename}"

    if not os.path.exists(file_path):
        raise HTTPException(status_code=404, detail="Content file not found. Upload it first.")

    content = parse_file(file_path)

    if not content:
        raise HTTPException(status_code=400, detail="Could not extract text from file.")

    if len(content.strip()) < 50:
        raise HTTPException(status_code=400, detail="Content too short to generate a paper.")

    paper = generate_full_paper(content, request.template)

    return {
        "status": "success",
        "template": request.template,
        "paper": paper
    }