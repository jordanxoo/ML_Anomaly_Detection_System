import aio_pika
from app.core.config import settings


rabbitmq_connection = None

async def get_rabbitmq_connection():
    global rabbitmq_connection
    if rabbitmq_connection is None or rabbitmq_connection.is_closed:
        rabbitmq_connection = await aio_pika.connect_robust(settings.RABBITMQ_URL)

    return rabbitmq_connection

