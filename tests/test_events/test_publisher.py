from unittest.mock import patch
from app.events.publisher import publish_order_event


def publish_order_event():
    with patch("app.events.publisher.redis_client.publish") as mock_publish:
        publish_order_event("order_created", {"order_id": 1})

        mock_publish.assert_called_once()