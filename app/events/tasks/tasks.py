import json
import uuid
import asyncio
import aioredis

from app.core.config import settings
from app.core.celery_app import celery_app

REDIS_URL = settings.REDIS_URL


class UUIDEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, uuid.UUID):
            return str(obj)
        return super().default(obj)


async def get_redis():
    return await aioredis.from_url(REDIS_URL, decode_responses=True)


@celery_app.task(name="publish_order_event_task")
def publish_order_event_task(order_payload: dict):
    """
    Celery task that publishes order event to Redis
    """

    async def _publish():
        redis = await get_redis()
        await redis.publish(
            "orders",
            json.dumps(order_payload, cls=UUIDEncoder)
        )

    asyncio.run(_publish())