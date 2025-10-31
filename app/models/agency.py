from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import String
from app.models.base import Base, TimestampMixin
from typing import Optional


class Agency(Base, TimestampMixin):
    __tablename__ = "agency"
    id: Mapped[str] = mapped_column(String(64), primary_key=True)
    name: Mapped[str] = mapped_column(String(255), index=True)
    country_code: Mapped[Optional[str]] = mapped_column(String(8), nullable=True)
    type: Mapped[Optional[str]] = mapped_column(String(128), nullable=True)