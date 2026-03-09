# import pytest
# from unittest.mock import AsyncMock, patch
# from httpx import AsyncClient
# from httpx._transports.asgi import ASGITransport  # ✅ Add this
# from fastapi import status
# from uuid import uuid4
# from datetime import datetime

# from app.main import app
# from app.orders.models import Order, OrderItem
# # ---------------------------
# # Fake user for tests
# # ---------------------------
# class FakeUser:
#     id = uuid4()
#     email = "test@test.com"
#     is_active = True

# async def fake_get_current_user():
#     return FakeUser()

# # Override current_user dependency
# from app.users.dependencies import get_current_user
# app.dependency_overrides[get_current_user] = fake_get_current_user

# # ---------------------------
# # Fake order fixture
# # ---------------------------
# @pytest.fixture
# def fake_order():
#     order = Order(
#         id=1,
#         customer_id=uuid4(),
#         restaurant_id=1,
#         status="PENDING",
#         total_amount=50.0,
#         created_at=datetime.utcnow(),
#         items=[
#             OrderItem(
#                 menu_item_id=1,
#                 quantity=2,
#                 price=25.0,
#                 menu_item=AsyncMock(name="Burger")
#             )
#         ],
#         restaurant=AsyncMock(name="Test Restaurant", id=1, owner_id=uuid4())
#     )
#     order.restaurant.name = "Test Restaurant"
#     for item in order.items:
#         item.menu_item.name = "Burger"
#     return order

# # ---------------------------
# # Patch OrderService and test routes
# # ---------------------------
# @pytest.mark.asyncio
# @patch("app.orders.router.OrderService.create_order", new_callable=AsyncMock)
# async def test_create_order(mock_create_order, fake_order):
#     mock_create_order.return_value = fake_order

#     async with AsyncClient(
#         transport=ASGITransport(app=app),
#         base_url="http://test"
#     ) as client:
#         response = await client.post(
#             "/orders/",
#             json={
#                 "restaurant_id": 1,
#                 "items": [{"menu_item_id": 1, "quantity": 2}]
#             }
#         )

#     assert response.status_code == status.HTTP_200_OK
#     data = response.json()
#     assert data["id"] == fake_order.id
#     assert data["restaurant_name"] == fake_order.restaurant.name
#     assert data["items"][0]["menu_item_name"] == "Burger"

# @pytest.mark.asyncio
# @patch("app.orders.router.OrderService.get_order", new_callable=AsyncMock)
# async def test_get_order(mock_get_order, fake_order):
#     mock_get_order.return_value = fake_order

#     async with AsyncClient(
#         transport=ASGITransport(app=app),
#         base_url="http://test"
#     ) as client:
#         response = await client.get("/orders/1")

#     assert response.status_code == status.HTTP_200_OK
#     data = response.json()
#     assert data["id"] == fake_order.id
#     assert data["status"] == fake_order.status

# @pytest.mark.asyncio
# @patch("app.orders.router.OrderService.complete_order", new_callable=AsyncMock)
# async def test_complete_order(mock_complete_order, fake_order):
#     fake_order.status = "COMPLETED"
#     mock_complete_order.return_value = fake_order

#     async with AsyncClient(
#         transport=ASGITransport(app=app),
#         base_url="http://test"
#     ) as client:
#         response = await client.post("/orders/complete/1")

#     assert response.status_code == status.HTTP_200_OK
#     data = response.json()
#     assert data["status"] == "COMPLETED"