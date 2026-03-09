from app.schemas.flow import NetworkFlow
from app.services.ml_service import ml_service
from fastapi import APIRouter, Depends, HTTPException, Query,Request
from app.schemas.alert import PredictResponse
from app.services.alert_service import save_alert
from app.core.database import get_db
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.security import get_current_user
from app.services.influx_serivce import write_flow_metric
from app.core.limiter import limiter
router = APIRouter()

@router.post("/predict",response_model=PredictResponse)
@limiter.limit("20/minute")
async def get_predict(request: Request,
                      flow : NetworkFlow,
                      db: AsyncSession = Depends(get_db),
                      user: str = Depends(get_current_user)):

        res = ml_service.predict(flow)
        await save_alert(flow,res,db)
        write_flow_metric(flow,res)
        return res
    