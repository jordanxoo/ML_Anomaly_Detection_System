from app.schemas.flow import NetworkFlow
from app.services.ml_service import ml_service
from fastapi import APIRouter, Depends, HTTPException, Query
from app.schemas.alert import PredictResponse
from app.services.alert_service import save_alert
from app.core.database import get_db
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.security import get_current_user

router = APIRouter()

@router.post("/predict",response_model=PredictResponse)
async def get_predict(flow : NetworkFlow,
                      db: AsyncSession = Depends(get_db),
                      user: str = Depends(get_current_user)):
    try:
        res = ml_service.predict(flow)
        await save_alert(flow,res,db)
        return res
    except Exception as e:
        raise HTTPException(500,e)
