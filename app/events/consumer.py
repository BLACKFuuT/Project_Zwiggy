# app/events/consumer.py

import aioredis
import asyncio
import json
from aiokafka import AIOKafkaConsumer  # ✅ correct
async def start_consumer():
    """
    Start a Redis consumer to process order events.
    """
    redis = aioredis.from_url("redis://redis:6379", encoding="utf-8", decode_responses=True)
    pubsub = redis.pubsub()
    await pubsub.subscribe("orders_channel")

    print(" Redis consumer started. Listening for order events...")

    async for message in pubsub.listen():
        if message['type'] == 'message':
            event = json.loads(message['data'])
            print(" Event received:", event)

            # React based on event type
            if event['event_type'] == 'order_created':
                # Example actions:
                print(f"Notify user {event['user_id']} about order {event['order_id']}")
                print(f" Update inventory for order {event['order_id']}")
            elif event['event_type'] == 'order_completed':
                print(f" Log completion for order {event['order_id']}")
                print(f"Trigger analytics for order {event['order_id']}")