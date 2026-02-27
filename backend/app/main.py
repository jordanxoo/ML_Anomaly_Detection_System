from contextlib import asynccontextmanager

from fastapi import FastAPI 
from fastapi.middleware.cors import CORSMiddleware

from app.core.config import settings
from app.core.database import engine,Base
from app.api import alert, predict

@asynccontextmanager
async def lifespan(app: FastAPI):
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield
