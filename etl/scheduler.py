import sys, pathlib, asyncio
sys.path.append(str(pathlib.Path(__file__).resolve().parents[1]))

from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.cron import CronTrigger
from etl.jobs import etl_upcoming_launches

async def job():
    try:
        n = await etl_upcoming_launches()
        print(f"[scheduler] ok, inserted/updated={n}")
    except Exception as e:
        print(f"[scheduler] failed: {e}")

if __name__ == "__main__":
    sched = AsyncIOScheduler(timezone="UTC")
    sched.add_job(job, CronTrigger(minute="*/10"))
    sched.start()
    print("[scheduler] started. Ctrl+C to exit.")
    asyncio.get_event_loop().run_forever()
