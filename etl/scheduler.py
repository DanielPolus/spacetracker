from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.interval import IntervalTrigger
import asyncio
from etl.incremental import run_incremental


async def job():
    loop = asyncio.get_event_loop()
    inserted = await loop.run_in_executor(None, run_incremental)
    print(f"[scheduler] inserted={inserted}")


if __name__ == "__main__":
    sched = AsyncIOScheduler(timezone="UTC")
    sched.add_job(job, IntervalTrigger(minutes=5))
    sched.start()

    print("[scheduler] started. Ctrl+C to exit.")
    try:
        asyncio.get_event_loop().run_forever()
    except (KeyboardInterrupt, SystemExit):
        pass
