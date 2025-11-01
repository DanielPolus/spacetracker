from sqlalchemy.dialects.postgresql import insert
from sqlalchemy.orm import Session
from app.models.agency import Agency
from app.models.rocket import Rocket
from app.models.launch import Launch
from typing import Optional

def upsert_agency(db: Session, agency_id: Optional[str], name: Optional[str]):
    if not agency_id:
        return
    stmt = insert(Agency).values(id=agency_id, name=(name or agency_id)[:255])
    stmt = stmt.on_conflict_do_update(
        index_elements=[Agency.id],
        set_={"name": (name or agency_id)[:255]}
    )
    db.execute(stmt)

def upsert_rocket(db: Session, rocket_id: Optional[str], name: Optional[str], agency_id: Optional[str]):
    if not rocket_id:
        return
    stmt = insert(Rocket).values(id=rocket_id, name=(name or rocket_id)[:255], agency_id=agency_id)
    stmt = stmt.on_conflict_do_update(
        index_elements=[Rocket.id],
        set_={"name": (name or rocket_id)[:255], "agency_id": agency_id}
    )
    db.execute(stmt)

def upsert_launch(db: Session, row: dict):
    stmt = insert(Launch).values(
        id=row["id"],
        name=row["name"],
        window_start=row["window_start"],
        status=row["status"],
        rocket_id=row["rocket_id"],
        agency_id=row["agency_id"],
        location=row["location"],
    )
    stmt = stmt.on_conflict_do_update(
        constraint="uq_launch_name_ts",
        set_={
            "status": row["status"],
            "rocket_id": row["rocket_id"],
            "agency_id": row["agency_id"],
            "location": row["location"],
            "window_start": row["window_start"],
        }
    )
    db.execute(stmt)
