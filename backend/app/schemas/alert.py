from datetime import datetime

from pydantic import BaseModel


class AlertBase(BaseModel):
    src_ip: str
    dst_ip: str
    src_port: int | None = None
    dst_port: int | None = None
    protocol: str | None = None
    anomaly_score: float
    attack_type: str | None = None
    confidence: float


class AlertCreate(AlertBase):
    pass


class AlertRead(AlertBase):
    id: int
    timestamp: datetime

    model_config = {"from_attributes": True}


class AlertList(BaseModel):
    total: int
    alerts: list[AlertRead]
