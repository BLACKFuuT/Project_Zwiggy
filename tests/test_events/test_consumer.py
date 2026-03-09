# tests/test_events/test_consumer.py
import pytest
from unittest.mock import patch, AsyncMock
from app.events.consumer import start_consumer

class AsyncIterator:
    def __init__(self, items):
        self._items = items

    def __aiter__(self):
        self._iter = iter(self._items)
        return self

    async def __anext__(self):
        try:
            return next(self._iter)
        except StopIteration:
            raise StopAsyncIteration

class FakePubSub:
    def __init__(self):
        self.channels = []
        self.listen_calls = 0
        self._messages = AsyncIterator([])

    async def subscribe(self, channel):
        self.channels.append(channel)

    def listen(self):
        self.listen_calls += 1
        return self._messages

class FakeRedis:
    def __init__(self):
        self._pubsub = FakePubSub()

    def pubsub(self):
        return self._pubsub

@pytest.mark.asyncio
@patch("app.events.consumer.aioredis.from_url")
async def test_start_consumer(mock_from_url):
    # Return our FakeRedis instance
    fake_redis = FakeRedis()
    mock_from_url.return_value = fake_redis

    # Run the consumer 
    await start_consumer()

    #  Check that subscribe was called
    assert "orders_channel" in fake_redis.pubsub().channels
    # Optionally check that listen was invoked
    assert fake_redis.pubsub().listen_calls == 1