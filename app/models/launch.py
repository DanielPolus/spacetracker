from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import String, DateTime, UniqueConstraint
from app.models.base import Base, TimestampMixin
from datetime import datetime
from typing import Optional


class Launch(Base, TimestampMixin):
    __tablename__ = "launch"
    id: Mapped[str] = mapped_column(String(64), primary_key=True)   # id из API
    name: Mapped[str] = mapped_column(String(255), index=True)
    window_start: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True), nullable=True)
    status: Mapped[Optional[str]] = mapped_column(String(64), nullable=True)
    rocket_id: Mapped[Optional[str]] = mapped_column(String(64), nullable=True)
    agency_id: Mapped[Optional[str]] = mapped_column(String(64), nullable=True)
    location: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)

    __table_args__ = (
        UniqueConstraint("name", "window_start", name="uq_launch_name_ts"),
    )
