from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import String, Integer, DateTime, func
from app.models.base import Base
from datetime import datetime
from typing import Optional


class ETLRun(Base):
    __tablename__ = "etl_run"
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    job: Mapped[str] = mapped_column(String(64))
    started_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    finished_at: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True), nullable=True)
    status: Mapped[str] = mapped_column(String(32), default="running")
    rows_ingested: Mapped[int] = mapped_column(Integer, default=0)
    error_text: Mapped[Optional[str]] = mapped_column(String(1000), nullable=True)
