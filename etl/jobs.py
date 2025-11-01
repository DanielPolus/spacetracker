import sys, pathlib, asyncio
sys.path.append(str(pathlib.Path(__file__).resolve().parents[1]))

from app.core.db import session_scope
from app.models.etl_run import ETLRun
from etl.source_ll import fetch_upcoming_all
from etl.normalize import norm_launch
from etl.etl_load import upsert_agency, upsert_rocket, upsert_launch

async def etl_upcoming_launches():
    rows_ingested = 0

    data = await fetch_upcoming_all()
    normalized = [norm_launch(x) for x in data]

    with session_scope() as s:
        run = ETLRun(job="upcoming_launches", status="running", rows_ingested=0)
        s.add(run); s.flush()
        try:
            for row in normalized:
                upsert_agency(s, row["agency_id"], row.get("_agency_name"))
                upsert_rocket(s, row["rocket_id"], row.get("_rocket_name"), row["agency_id"])
                upsert_launch(s, row)
                rows_ingested += 1
            run.status = "success"
            run.rows_ingested = rows_ingested
        except Exception as e:
            run.status = "failed"
            run.error_text = str(e)[:1000]
            raise
    return rows_ingested
