from fastapi import APIRouter, Request
from fastapi.templating import Jinja2Templates
from pathlib import Path

router = APIRouter(tags=["ui"])

TEMPLATES_DIR = Path(__file__).resolve().parents[2] / "templates"
templates = Jinja2Templates(directory=str(TEMPLATES_DIR))

@router.get("/dashboard")
def dashboard(request: Request):
    return templates.TemplateResponse("dashboard.html", {"request": request})
