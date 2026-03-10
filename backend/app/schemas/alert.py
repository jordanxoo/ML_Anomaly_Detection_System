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

class PredictResponse(BaseModel):
    is_anomaly : bool
    anomaly_score : float
    confidence : float
    attack_type : str | None = None


class Stats(BaseModel):
    value: str
    count: int

class AttacksStats(BaseModel):
    top_src_ips : list[Stats]
    top_dst_ips: list[Stats]
    top_attack_types: list[Stats]

