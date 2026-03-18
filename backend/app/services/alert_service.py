from sqlalchemy.ext.asyncio import AsyncSession
from app.models.alert import Alert
from app.schemas.flow import NetworkFlow

async def save_alert(flow: NetworkFlow,prediction: dict, db: AsyncSession):
    
    if prediction["is_anomaly"]:
        alert = Alert(
            src_ip = flow.src_ip,dst_ip = flow.dst_ip,
                      src_port = flow.src_port, dst_port = flow.dst_port,
                      anomaly_score = prediction["anomaly_score"],
                      attack_type = prediction["attack_type"],
                      confidence = prediction["confidence"])
        
        db.add(alert)
        await db.commit()
        