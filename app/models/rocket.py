from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import String
from app.models.base import Base, TimestampMixin
from typing import Optional


class Rocket(Base, TimestampMixin):
    __tablename__ = "rocket"
    id: Mapped[str] = mapped_column(String(64), primary_key=True)
    name: Mapped[str] = mapped_column(String(255), index=True)
    agency_id: Mapped[Optional[str]] = mapped_column(String(64), nullable=True)