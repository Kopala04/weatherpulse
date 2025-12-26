from sqlalchemy import String, Integer, DateTime, func
from sqlalchemy.orm import Mapped, mapped_column
from app.core.db import Base

class Favorite(Base):
    __tablename__ = "favorites"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    city: Mapped[str] = mapped_column(String(100), index=True)
    lat: Mapped[float | None]
    lon: Mapped[float | None]
    created_at: Mapped[DateTime] = mapped_column(DateTime(timezone=True), server_default=func.now())
