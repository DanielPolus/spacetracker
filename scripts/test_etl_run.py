import sys, pathlib
sys.path.append(str(pathlib.Path(__file__).resolve().parents[1]))

from app.core.db import session_scope
from app.models.etl_run import ETLRun
from sqlalchemy import select

def demo():
    with session_scope() as s:
        run = ETLRun(job="seed_agencies", status="running", rows_ingested=0)
        s.add(run)
        s.flush()
        run.status = "success"
        run.rows_ingested = 3

    with session_scope() as s:
        rows = s.execute(select(ETLRun).order_by(ETLRun.id.desc()).limit(5)).scalars().all()
        for r in rows:
            print(r.id, r.job, r.status, r.rows_ingested, r.started_at, r.finished_at)

if __name__ == "__main__":
    demo()
