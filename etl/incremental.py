import httpx
from datetime import datetime
from app.core.db import session_scope
from app.models.launch import Launch
from app.models.etl_run import ETLRun
from typing import Optional


API_URL = "https://ll.thespacedevs.com/2.2.0/launch/upcoming/?limit=50"


def _parse_dt(s: Optional[str]):
    if not s:
        return None
    return datetime.fromisoformat(s.replace("Z", "+00:00"))


def extract_upcoming():
    with httpx.Client(timeout=30) as client:
        r = client.get(API_URL)
        r.raise_for_status()
        data = r.json()
        return data.get("results", [])


def transform(records: list[dict]) -> list[dict]:
    out: list[dict] = []
    for it in records:
        launch_id = it.get("id")
        name = it.get("name") or ""
        window_start = _parse_dt(it.get("window_start"))
        status = (it.get("status") or {}).get("name")
        rocket_cfg = ((it.get("rocket") or {}).get("configuration") or {})
        rocket_id = rocket_cfg.get("id")
        rocket_name = rocket_cfg.get("name")
        pad = it.get("pad") or {}
        location_name = (pad.get("location") or {}).get("name")

        agency = (it.get("launch_service_provider") or {})
        agency_id = agency.get("id")
        agency_name = agency.get("name")
        agency_type = agency.get("type")
        agency_cc = agency.get("country_code")

        out.append({
            "launch": {
                "id": str(launch_id),
                "name": name,
                "window_start": window_start,
                "status": status,
                "rocket_id": str(rocket_id) if rocket_id is not None else None,
                "agency_id": str(agency_id) if agency_id is not None else None,
                "location": location_name,
            },
            "rocket": {
                "id": str(rocket_id) if rocket_id is not None else None,
                "name": rocket_name,
                "agency_id": str(agency_id) if agency_id is not None else None,
            },
            "agency": {
                "id": str(agency_id) if agency_id is not None else None,
                "name": agency_name,
                "type": agency_type,
                "country_code": agency_cc,
            }
        })
    return out


def load(rows: list[dict]) -> int:
    """Простейший upsert по первичным ключам (SQLAlchemy merge)."""
    from app.models.agency import Agency
    from app.models.rocket import Rocket

    inserted = 0
    with session_scope() as db:
        run = ETLRun(job="incremental_upcoming")
        db.add(run)
        db.flush()

        try:
            for row in rows:
                ag = row["agency"]
                if ag["id"]:
                    db.merge(Agency(**ag)) 

                rk = row["rocket"]
                if rk["id"]:
                    db.merge(Rocket(**rk))

                ln = row["launch"]
                db.merge(Launch(**ln))
                inserted += 1

            run.status = "success"
            run.rows_ingested = inserted
        except Exception as e:
            run.status = "failed"
            run.error_text = str(e)
            raise
    return inserted


def run_incremental() -> int:
    src = extract_upcoming()
    rows = transform(src)
    return load(rows)
