from __future__ import annotations
from typing import Optional
import asyncio
from datetime import datetime, timezone

from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.cron import CronTrigger

from etl.jobs import etl_upcoming_launches

_scheduler: Optional[AsyncIOScheduler] = None
_job_id = "etl_upcoming_every_minute"

def get_scheduler() -> AsyncIOScheduler:
    global _scheduler
    if _scheduler is None:
        loop = asyncio.get_running_loop()
        _scheduler = AsyncIOScheduler(timezone="UTC", event_loop=loop)
    return _scheduler

def is_running() -> bool:
    return get_scheduler().running

def ensure_job_exists() -> None:
    sch = get_scheduler()
    if sch.get_job(_job_id) is None:
        sch.add_job(
            _run_etl_wrapper,
            CronTrigger(minute="*"),
            id=_job_id,
            replace_existing=True,
        )

async def _run_etl_wrapper():
    await etl_upcoming_launches()

async def start_scheduler() -> None:
    sch = get_scheduler()
    ensure_job_exists()
    if not sch.running:
        sch.start()

async def stop_scheduler() -> None:
    sch = get_scheduler()
    if sch.running:
        sch.shutdown(wait=False)

def next_run_time_str() -> Optional[str]:
    try:
        sch = get_scheduler()
        job = sch.get_job(_job_id)
        if not job:
            return None

        nrt = getattr(job, "next_run_time", None)

        if not nrt and hasattr(job, "trigger") and hasattr(job.trigger, "get_next_fire_time"):
            now = datetime.now(timezone.utc)
            nrt = job.trigger.get_next_fire_time(None, now)

        return nrt.isoformat() if nrt else None
    except Exception:
        return None
