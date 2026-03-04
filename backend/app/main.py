from contextlib import asynccontextmanager
import logging
from fastapi import FastAPI 
from fastapi.middleware.cors import CORSMiddleware
from  app.services.ml_service import ml_service
from app.core.config import settings
from app.core.database import engine,Base
from app.api import alerts, predict

logging.basicConfig(level=logging.DEBUG)

@asynccontextmanager
async def lifespan(app: FastAPI):
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    ml_service.load()
    yield

app = FastAPI(lifespan=lifespan)
app.include_router(router=alerts.router)
app.include_router(router=predict.router)

