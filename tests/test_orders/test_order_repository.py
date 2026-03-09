# # tests/test_orders/test_order_repository.py

# import pytest
# from unittest.mock import AsyncMock, patch
# from decimal import Decimal
# from uuid import uuid4
# from sqlalchemy.ext.asyncio import AsyncSession
# from app.orders.models import Order, OrderItem
# from app.menu_items.models import MenuItem
# from app.restaurants.models import Restaurant
# from app.users.models import User
# from app.orders.repository import OrderRepository

# @pytest.fixture
# def repo():
#     return OrderRepository()

# @pytest.fixture
# def fake_user():
#     return User(id=uuid4(), email="user@test.com", password="hashed")

# @pytest.fixture
# def fake_restaurant():
#     return Restaurant(id=1, name="Test Restaurant")

# @pytest.fixture
# def fake_menu_item():
#     return MenuItem(id=1, name="Burger", price=Decimal("10.0"))

# @pytest.mark.asyncio
# async def test_create_order(repo):
#     db = AsyncMock(spec=AsyncSession)
#     order = Order(id=1, customer_id=uuid4(), restaurant_id=1, status="PENDING")
    
#     db.flush = AsyncMock()
#     db.add = AsyncMock()

#     result = await repo.create_order(db, order)

#     db.add.assert_called_once_with(order)
#     db.flush.assert_awaited_once()
#     assert result == order

# @pytest.mark.asyncio
# async def test_create_order_item(repo, fake_menu_item):
#     db = AsyncMock(spec=AsyncSession)
#     order_item = OrderItem(id=1, order_id=1, menu_item=fake_menu_item, quantity=2, price=Decimal("20.0"))

#     db.flush = AsyncMock()
#     db.add = AsyncMock()

#     result = await repo.create_order_item(db, order_item)

#     db.add.assert_called_once_with(order_item)
#     db.flush.assert_awaited_once()
#     assert result == order_item

# @pytest.mark.asyncio
# async def test_update_order_total(repo):
#     db = AsyncMock(spec=AsyncSession)
#     db.execute = AsyncMock()

#     await repo.update_order_total(db, order_id=1, total=50.0)
#     db.execute.assert_awaited_once()
#     args = db.execute.call_args[0][0].compile().params
#     assert args["total_amount"] == 50.0

# @pytest.mark.asyncio
# async def test_update_status(repo):
#     db = AsyncMock(spec=AsyncSession)
#     db.execute = AsyncMock()

#     await repo.update_status(db, order_id=1, status="COMPLETED")
#     db.execute.assert_awaited_once()
#     args = db.execute.call_args[0][0].compile().params
#     assert args["status"] == "COMPLETED"