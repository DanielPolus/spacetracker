from fastapi import APIRouter
from app.services.scheduler_service import (
    start_scheduler, stop_scheduler, is_running, next_run_time_str, ensure_job_exists
)

router = APIRouter(tags=["scheduler"])

@router.get("/status")
async def scheduler_status():
    ensure_job_exists()
    return {"running": is_running(), "next": next_run_time_str()}

@router.post("/start")
async def scheduler_start():
    await start_scheduler()
    return {"running": True, "next": next_run_time_str()}

@router.post("/stop")
async def scheduler_stop():
    await stop_scheduler()
    return {"running": False, "next": None}
