from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy import func,select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db
from app.models.alert import Alert
from app.schemas.alert import AlertList, AlertRead

router = APIRouter()

@router.get("/",response_model=AlertList)
async def list_alerts(
    skip: int = Query(0,ge=0),
    limit: int = Query(50,ge = 1,le=500),
    db: AsyncSession = Depends(get_db)
):
    total = await db.scalar(select(func.count()).select_from(Alert))
    result = await db.execute(select(Alert).order_by(Alert.timestamp.desc()).offset(skip).limit(limit))
    alerts = result.scalars().all()

    return AlertList(total=total,alerts=alerts)

@router.get("/{alert_id}",response_model=AlertRead)
async def get_alert(alert_id : int, 
                    db: AsyncSession = Depends(get_db)):
    
    alert = await db.get(Alert,alert_id)
    if alert is None:
        raise HTTPException(status_code=404,detail='...')
    else:
        return alert

