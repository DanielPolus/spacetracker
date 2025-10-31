from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.core.db import SessionLocal
from app.models.launch import Launch

router = APIRouter()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.get("/health")
def health():
    return {"status": "ok"}


@router.get("/launches")
def list_launches(limit: int = 20, db: Session = Depends(get_db)):
    q = db.query(Launch).order_by(Launch.window_start.desc().nullslast()).limit(limit)
    return [
        {
            "id": x.id,
            "name": x.name,
            "window_start": x.window_start,
            "status": x.status,
            "rocket_id": x.rocket_id,
            "agency_id": x.agency_id,
            "location": x.location,
        }
        for x in q
    ]
