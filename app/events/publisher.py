import json
import asyncio
import aioredis  # Async Redis client
import uuid  # Needed for UUID type check

# Redis URL (change if needed)
REDIS_URL = "redis://localhost:6379/0"

# Singleton Redis connection
_redis = None

async def get_redis():
    global _redis
    if _redis is None:
        _redis = await aioredis.from_url(REDIS_URL, decode_responses=True)
    return _redis

class UUIDEncoder(json.JSONEncoder):
    """Custom JSON encoder to convert UUIDs to strings."""
    def default(self, obj):
        if isinstance(obj, uuid.UUID):
            return str(obj)
        return super().default(obj)

async def publish_order_event(order, order_items, event_type: str):
    """
    Publishes an order event to Redis channel.
    order_items: list of OrderItem objects (already collected)
    """
    redis = await get_redis()

    # Prepare payload
    payload = {
        "event_type": event_type,
        "order_id": order.id,
        "customer_id": order.customer_id,
        "restaurant_id": order.restaurant_id,
        "status": order.status,
        "total_amount": float(order.total_amount),
        "items": [
            {
                "menu_item_id": item.menu_item_id,
                "quantity": item.quantity,
                "price": float(item.price)
            } for item in order_items
        ]
    }

    # Publish asynchronously with custom UUID encoder
    await redis.publish("orders", json.dumps(payload, cls=UUIDEncoder)) 