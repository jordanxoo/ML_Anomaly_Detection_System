from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy import func,select
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.database import get_db
from app.models.alert import Alert
from app.schemas.alert import AlertList, AlertRead, AttacksStats
from app.core.security import get_current_user
from app.schemas.alert import Stats
from datetime import datetime
router = APIRouter()

@router.get("/",response_model=AlertList)
async def list_alerts(
    skip: int = Query(0,ge=0),
    limit: int = Query(50,ge = 1,le=500),
    db: AsyncSession = Depends(get_db),
    user: str = Depends(get_current_user),
    src_ip: str | None = Query(None),
    dst_ip: str | None = Query(None),
    attack_type: str | None = Query(None),
    protocol: str | None = Query(None),
    date_from: datetime | None = Query(None),
    date_to: datetime | None = Query(None)
):
    query = select(Alert)
    if src_ip:
        query = query.where(Alert.src_ip == src_ip)
    if dst_ip:
        query = query.where(Alert.dst_ip == dst_ip)
    if attack_type:
        query = query.where(Alert.attack_type == attack_type)
    if protocol:
        query = query.where(Alert.protocol == protocol)
    if date_from:
        query = query.where(Alert.timestamp >= date_from)
    if date_to:
        query = query.where(Alert.timestamp < date_to)

    total = await db.scalar(select(func.count()).select_from(query.subquery()))
    result = await db.execute(query.order_by(Alert.timestamp.desc()).offset(skip).limit(limit))
    alerts = result.scalars().all()

    return AlertList(total=total,alerts=alerts)

@router.get("/stats", response_model= AttacksStats)
async def get_stats(db : AsyncSession = Depends(get_db),
                    user: str = Depends(get_current_user)):
    
    
    src_ip = select(Alert.src_ip,func.count().label('count')
                    ).group_by(Alert.src_ip).order_by(func.count().desc()
                    ).limit(5)
    dst_ip = select(Alert.dst_ip,func.count().label('count')
                    ).group_by(Alert.dst_ip).order_by(func.count().desc()
                    ).limit(5)

    attack_type = select(Alert.attack_type,func.count().label('count')
                        ).group_by(Alert.attack_type).order_by(func.count().desc()
                        ).limit(5)

    result_src_ip = await db.execute(src_ip)
    result_dst_ip = await db.execute(dst_ip)
    result_attack_type = await db.execute(attack_type)

    src_ip_stats_list = [Stats(value=row[0],count=row[1]) for row in result_src_ip.all()]
    dst_ip_stats_list = [Stats(value=row[0],count = row[1]) for row in result_dst_ip.all()]
    result_attack_type_list = [Stats(value=row[0],count=row[1]) for row in result_attack_type.all()]

    return AttacksStats(top_src_ips = src_ip_stats_list, 
                        top_dst_ips = dst_ip_stats_list,
                        top_attack_types = result_attack_type_list)


@router.get("/{alert_id}",response_model=AlertRead)
async def get_alert(alert_id : int, 
                    db: AsyncSession = Depends(get_db),
                    user: str = Depends(get_current_user)):
    
    alert = await db.get(Alert,alert_id)
    if alert is None:
        raise HTTPException(status_code=404,detail='...')
    else:
        return alert

