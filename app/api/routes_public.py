from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.core.db import SessionLocal
from app.models.launch import Launch

router = APIRouter(prefix="/public", tags=["public"])

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.get("/launches")
def list_launches(limit: int = 20, db: Session = Depends(get_db)):
    q = db.query(Launch).order_by(Launch.window_start.desc()).limit(limit)
    items = q.all()
    return [
        {
            "id": x.id, "name": x.name, "time": x.window_start,
            "status": x.status, "rocket_id": x.rocket_id,
            "agency_id": x.agency_id, "location": x.location
        } for x in items
    ]
