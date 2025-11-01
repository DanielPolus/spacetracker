from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.core.db import SessionLocal
from app.models.etl_run import ETLRun

router = APIRouter(prefix="/metrics", tags=["metrics"])

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.get("/etl")
def etl_metrics(db: Session = Depends(get_db)):
    runs = db.query(ETLRun).order_by(ETLRun.started_at.desc()).limit(20).all()
    return [
        {
            "id": r.id,
            "job": r.job,
            "started_at": r.started_at,
            "finished_at": r.finished_at,
            "status": r.status,
            "rows_ingested": r.rows_ingested,
            "error_text": r.error_text,
        }
        for r in runs
    ]
