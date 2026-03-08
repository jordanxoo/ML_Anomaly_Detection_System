from contextlib import asynccontextmanager
import logging
from fastapi import FastAPI 
from slowapi import _rate_limit_exceeded_handler
from app.core.limiter import limiter
from slowapi.errors import RateLimitExceeded
from fastapi.middleware.cors import CORSMiddleware
from  app.services.ml_service import ml_service
from app.core.config import settings
from app.core.database import engine,Base
from app.api import alerts, predict
from app.api import auth
from app.services.redis_consumer import consume_redis
import asyncio
logging.basicConfig(level=logging.DEBUG)

@asynccontextmanager
async def lifespan(app: FastAPI):
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    ml_service.load()
    asyncio.create_task(consume_redis())
    yield

app = FastAPI(lifespan=lifespan)
app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded,_rate_limit_exceeded_handler)
app.include_router(router=alerts.router)
app.include_router(router=predict.router)
app.include_router(router=auth.router,prefix="/auth")
