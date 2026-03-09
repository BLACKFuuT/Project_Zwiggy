# tests/test_orders/test_order_service.py

import pytest
from unittest.mock import AsyncMock, patch, MagicMock
from uuid import uuid4
from datetime import datetime
from fastapi import HTTPException

from app.orders.service import OrderService
from app.orders.models import Order, OrderItem
from app.orders.schemas import OrderCreate
from app.users.models import User

# ---------------------------
# Fixtures
# ---------------------------
@pytest.fixture
def fake_user():
    return User(id=uuid4(), email="test@test.com")

@pytest.fixture
def fake_order(fake_user):
    return Order(
        id=1,
        customer_id=fake_user.id,
        restaurant_id=1,
        status="PENDING",
        total_amount=50.0,
        created_at=datetime.utcnow(),
        items=[OrderItem(menu_item_id=1, quantity=2, price=25.0)],
        restaurant=MagicMock(id=1, owner_id=fake_user.id)
    )

# ---------------------------
# Test create_order
# ---------------------------
@pytest.mark.asyncio
@patch("app.orders.service.RestaurantRepository.get_by_id", new_callable=AsyncMock)
@patch("app.orders.service.MenuItemRepository.get_by_id", new_callable=AsyncMock)
@patch("app.orders.service.OrderRepository.create_order", new_callable=AsyncMock)
@patch("app.orders.service.OrderRepository.create_order_item", new_callable=AsyncMock)
@patch("app.orders.service.OrderRepository.update_order_total", new_callable=AsyncMock)
@patch("app.orders.service.publish_order_event_task.delay")
@patch("app.orders.service.send_order_email.delay")
async def test_create_order(
    mock_send_email,
    mock_publish_event,
    mock_update_total,
    mock_create_item,
    mock_create_order,
    mock_get_menu,
    mock_get_restaurant,
    fake_user
):
    service = OrderService()

    # Arrange repository mocks
    mock_get_restaurant.return_value = AsyncMock(id=1, owner_id=fake_user.id)
    mock_get_menu.return_value = AsyncMock(price=25.0)
    mock_create_order.return_value = AsyncMock()
    mock_create_item.return_value = AsyncMock()

    fake_order_data = OrderCreate(
        restaurant_id=1,
        items=[{"menu_item_id": 1, "quantity": 2}]
    )

    # Proper fake order object for the DB mock
    fake_order_obj = Order(
        id=1,
        customer_id=fake_user.id,
        restaurant_id=1,
        status="PENDING",
        total_amount=50.0,
        created_at=datetime.utcnow(),
        items=[OrderItem(menu_item_id=1, quantity=2, price=25.0)],
        restaurant=MagicMock(id=1, owner_id=fake_user.id)
    )

    fake_result = MagicMock()
    fake_result.scalars.return_value.first.return_value = fake_order_obj

    fake_db = AsyncMock()
    fake_db.execute.return_value = fake_result

    # Act
    result = await service.create_order(fake_db, fake_order_data, fake_user)

    # Assert repository calls
    mock_get_restaurant.assert_awaited_once()
    mock_get_menu.assert_awaited_once()
    mock_create_order.assert_awaited_once()
    mock_create_item.assert_awaited_once()
    mock_update_total.assert_awaited_once()
    mock_send_email.assert_called_once()
    mock_publish_event.assert_called_once()


# ---------------------------
# Test get_order not found
# ---------------------------
@pytest.mark.asyncio
async def test_get_order_not_found(fake_user):
    service = OrderService()

    # Mock DB execute returning None
    fake_result = MagicMock()
    fake_result.scalars.return_value.first.return_value = None

    fake_db = AsyncMock()
    fake_db.execute.return_value = fake_result

    with pytest.raises(HTTPException) as exc_info:
        await service.get_order(fake_db, order_id=1, current_user=fake_user)

    assert exc_info.value.status_code == 404


# ---------------------------
# Test complete_order not authorized
# ---------------------------
@pytest.mark.asyncio
async def test_complete_order_not_authorized(fake_user, fake_order):
    service = OrderService()

    # Mock DB execute returning the fake_order
    fake_result = MagicMock()
    fake_result.scalars.return_value.first.return_value = fake_order

    fake_db = AsyncMock()
    fake_db.execute.return_value = fake_result

    # Set restaurant owner to someone else
    fake_order.restaurant.owner_id = uuid4()

    with pytest.raises(HTTPException) as exc_info:
        await service.complete_order(fake_db, order_id=1, current_user=fake_user)

    assert exc_info.value.status_code == 403