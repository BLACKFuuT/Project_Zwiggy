# # tests/test_orders/test_order_model.py

# import pytest
# from datetime import datetime
# from uuid import uuid4
# from decimal import Decimal

# from app.orders.models import Order, OrderItem
# from app.menu_items.models import MenuItem
# from app.users.models import User
# from app.restaurants.models import Restaurant

# @pytest.fixture
# def fake_user():
#     return User(id=uuid4(), email="testuser@example.com", password="hashedpassword")

# @pytest.fixture
# def fake_restaurant():
#     return Restaurant(id=1, name="Test Restaurant")

# @pytest.fixture
# def fake_menu_item():
#     return MenuItem(id=1, name="Pizza", price=Decimal("9.99"))

# @pytest.fixture
# def fake_order(fake_user, fake_restaurant):
#     return Order(
#         id=1,
#         customer_id=fake_user.id,
#         restaurant_id=fake_restaurant.id,
#         status="PENDING",
#         total_amount=0
#     )

# @pytest.fixture
# def fake_order_item(fake_order, fake_menu_item):
#     return OrderItem(
#         id=1,
#         order=fake_order,
#         menu_item=fake_menu_item,
#         quantity=2,
#         price=fake_menu_item.price * 2
#     )

# def test_order_creation(fake_order):
#     assert fake_order.status == "PENDING"
#     assert fake_order.total_amount == 0
#     assert fake_order.customer_id is not None
#     assert fake_order.restaurant_id is not None
#     assert fake_order.created_at is None or isinstance(fake_order.created_at, datetime)

# def test_order_item_relationship(fake_order_item, fake_order, fake_menu_item):
#     # Check that the order item links to the order
#     assert fake_order_item.order == fake_order
#     # Check that the order item links to the menu item
#     assert fake_order_item.menu_item == fake_menu_item
#     # Check price and quantity
#     assert fake_order_item.quantity == 2
#     assert fake_order_item.price == fake_menu_item.price * 2

# def test_order_items_list(fake_order, fake_order_item):
#     # Add item to order
#     fake_order.items.append(fake_order_item)
#     assert len(fake_order.items) == 1
#     assert fake_order.items[0] == fake_order_item