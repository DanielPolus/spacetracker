from fastapi import APIRouter
from etl.jobs import etl_upcoming_launches

router = APIRouter(prefix="/etl", tags=["etl"])

@router.post("/run/upcoming")
async def run_upcoming():
    n = await etl_upcoming_launches()
    return {"status": "ok", "rows": n}
