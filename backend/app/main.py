from contextlib import asynccontextmanager
from fastapi import FastAPI, HTTPException
from slowapi import _rate_limit_exceeded_handler
from app.core.limiter import limiter
from slowapi.errors import RateLimitExceeded
from fastapi.middleware.cors import CORSMiddleware
from  app.services.ml_service import ml_service
from app.core.config import settings
from app.api import alerts, predict,websocket,auth
from app.services.redis_consumer import consume_redis
from app.core.exception_handlers import http_exception_handler, unhandled_exception_handler
import asyncio
from app.services.rabbitmq_consumer import consume_rabbitmq
from app.core.logging import configure_logging
from prometheus_fastapi_instrumentator import Instrumentator
configure_logging(debug=settings.DEBUG)

@asynccontextmanager
async def lifespan(app: FastAPI):
    ml_service.load()
    asyncio.create_task(consume_redis())
    asyncio.create_task(consume_rabbitmq())
    yield

app = FastAPI(lifespan=lifespan)
app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded,_rate_limit_exceeded_handler)
app.add_exception_handler(HTTPException,http_exception_handler)
app.add_exception_handler(Exception,unhandled_exception_handler)
app.add_middleware(CORSMiddleware,
                   allow_origins=settings.ALLOWED_ORIGINS,
                   allow_credentials= True,
                   allow_methods = ["*"],
                   allow_headers=["*"])

Instrumentator().instrument(app).expose(app)
app.include_router(router=alerts.router)
app.include_router(router=predict.router)
app.include_router(router=auth.router,prefix="/auth")
app.include_router(router=websocket.router)
