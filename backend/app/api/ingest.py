from fastapi import APIRouter
from app.schemas.flow import NetworkFlow
import aio_pika
from app.core.rabbitmq import get_rabbitmq_connection

router = APIRouter()


@router.post("/ingest")
async def publish_flow(flow : NetworkFlow):
    connection = await get_rabbitmq_connection()

    channel = await connection.channel()

    await channel.default_exchange.publish(
        aio_pika.Message(body=flow.model_dump_json().encode()),
        routing_key="network_flows"
    )

    return {"status":"queued"}



