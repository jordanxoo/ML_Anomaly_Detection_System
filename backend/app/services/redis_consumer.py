import redis
from app.core.config  import settings
import json
from app.schemas.flow import NetworkFlow
from app.services.ml_service import ml_service
from app.core.database import AsyncSessionLocal
from app.services.alert_service import save_alert
import asyncio
import logging
from app.services.influx_serivce import write_flow_metric
async def consume_redis():
    while True:
        try:
            r = redis.asyncio.Redis.from_url(settings.REDIS_URL)
            pubsub = r.pubsub()
            await pubsub.subscribe(settings.REDIS_CHANNEL)

            async for message in pubsub.listen():
                if message["type"] == "message":
                    try:
                        logging.info("Raw message: %s", message["data"])                                         

                        msg_dec = json.loads(message["data"].decode("utf-8"))
                        network_flow = NetworkFlow.model_validate(msg_dec)
                        prediction = ml_service.predict(network_flow)
                        write_flow_metric(network_flow,prediction)

                        async with AsyncSessionLocal() as db:
                            await save_alert(network_flow,prediction,db)
                    except Exception as ex:
                        logging.error("Failed to process message: %s",ex)
        except Exception as e:
            logging.error("Redis consumer error: %s",e)
            await asyncio.sleep(5)        
        