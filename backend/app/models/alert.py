from datetime import datetime

from sqlalchemy import DateTime, Float, Integer, String
from sqlalchemy.orm import Mapped, mapped_column

from app.core.database import Base


class Alert(Base):
    """Stores detected network anomaly alerts."""

    __tablename__ = "alerts"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    timestamp: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    src_ip: Mapped[str] = mapped_column(String(45))  # IPv4 or IPv6
    dst_ip: Mapped[str] = mapped_column(String(45))
    src_port: Mapped[int] = mapped_column(Integer, nullable=True)
    dst_port: Mapped[int] = mapped_column(Integer, nullable=True)
    protocol: Mapped[str] = mapped_column(String(10), nullable=True)
    anomaly_score: Mapped[float] = mapped_column(Float)
    attack_type: Mapped[str] = mapped_column(String(64), nullable=True)
    confidence: Mapped[float] = mapped_column(Float)
