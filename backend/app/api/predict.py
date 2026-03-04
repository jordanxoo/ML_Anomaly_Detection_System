from app.schemas.flow import NetworkFlow
from app.services.ml_service import ml_service
from fastapi import APIRouter, Depends, HTTPException, Query
from app.schemas.alert import PredictResponse

router = APIRouter()

@router.post("/predict",response_model=PredictResponse)
async def get_predict(flow : NetworkFlow):
    
    try:
        res = ml_service.predict(flow)
        return res
    except Exception as e:
        raise HTTPException(500,e)
