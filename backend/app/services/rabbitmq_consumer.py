import aio_pika
from app.core.config import settings
import logging
import json
from app.schemas.flow import NetworkFlow
from app.services.ml_service import ml_service
from app.services.influx_serivce import write_flow_metric
from app.services.alert_service import save_alert
from app.core.database import AsyncSessionLocal

async def consume_rabbitmq():

    connection = await aio_pika.connect_robust(settings.RABBITMQ_URL)
    channel = await connection.channel()
    queue = await channel.declare_queue("network_flows")

    async for message in queue:
        
        logging.info("raw message: %s", message.body)
        try:
            msg_dec = json.loads(message.body.decode("utf-8"))
            network_flow = NetworkFlow.model_validate(msg_dec)
            prediction = ml_service.predict(network_flow)
            write_flow_metric(network_flow,prediction=prediction)
            await message.ack()   

            async with AsyncSessionLocal() as db:
                await save_alert(network_flow,prediction,db)
     
        except Exception as e:
            await message.nack()
            logging.info("Failed to process RABBITMQ message: %s", e)
        

        


        
