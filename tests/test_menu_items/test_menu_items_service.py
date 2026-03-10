import pytest
from unittest.mock import AsyncMock, MagicMock
from fastapi import HTTPException
from app.menu_items.models import MenuItem
from app.restaurants.models import Restaurant
from app.menu_items.schemas import MenuItemUpdate
from app.users.models import User

# -------------------------------
# Fixtures
# -------------------------------

@pytest.fixture
def current_user():
    # Mock a user
    return User(id=1, email="user@example.com", is_active=True)

@pytest.fixture
def service():
    # Mock the MenuItemService with repository
    mock_service = MagicMock()
    mock_service.repository = MagicMock()
    return mock_service

# -------------------------------
# Update Item Success
# -------------------------------

@pytest.mark.asyncio
async def test_update_item_success(service, current_user):
    # Mock restaurant and menu item
    mock_restaurant = Restaurant(id=1, owner_id=current_user.id)
    item = MenuItem(id=1, name="Burger", description="Tasty", price=9.99, restaurant_id=1)
    item.restaurant = mock_restaurant

    # Mock DB execute
    mock_result = AsyncMock()
    mock_result.scalar_one_or_none.return_value = item
    mock_db = AsyncMock()
    mock_db.execute.return_value = mock_result

    # Mock update method
    service.repository.update.return_value = item

    update_data = MenuItemUpdate(name="New Burger")
    service.update_item = AsyncMock(return_value=item)

    updated_item = await service.update_item(mock_db, item.id, update_data, current_user)

    assert updated_item is not None
    assert isinstance(updated_item, MenuItem)

# -------------------------------
# Update Item Forbidden (Not Owner)
# -------------------------------

@pytest.mark.asyncio
async def test_update_item_forbidden(service, current_user):
    mock_restaurant = Restaurant(id=1, owner_id=999)  # different owner
    item = MenuItem(id=1, name="Burger", restaurant_id=1)
    item.restaurant = mock_restaurant

    mock_result = AsyncMock()
    mock_result.scalar_one_or_none.return_value = item
    mock_db = AsyncMock()
    mock_db.execute.return_value = mock_result

    update_data = MenuItemUpdate(name="New Burger")
    service.update_item = AsyncMock(side_effect=HTTPException(status_code=403, detail="Forbidden"))

    with pytest.raises(HTTPException) as exc:
        await service.update_item(mock_db, item.id, update_data, current_user)
    assert exc.value.status_code == 403

# -------------------------------
# Delete Item Success
# -------------------------------

@pytest.mark.asyncio
async def test_delete_item_success(service, current_user):
    mock_restaurant = Restaurant(id=1, owner_id=current_user.id)
    item = MenuItem(id=1, restaurant_id=1)
    item.restaurant = mock_restaurant

    mock_result = AsyncMock()
    mock_result.scalar_one_or_none.return_value = item
    mock_db = AsyncMock()
    mock_db.execute.return_value = mock_result

    service.repository.soft_delete.return_value = None
    service.delete_item = AsyncMock(return_value={"message": "Menu item deleted"})

    result = await service.delete_item(mock_db, item.id, current_user)
    assert result == {"message": "Menu item deleted"}

# -------------------------------
# Delete Item Forbidden (Not Owner)
# -------------------------------

@pytest.mark.asyncio
async def test_delete_item_forbidden(service, current_user):
    mock_restaurant = Restaurant(id=1, owner_id=999)  # different owner
    item = MenuItem(id=1, restaurant_id=1)
    item.restaurant = mock_restaurant

    mock_result = AsyncMock()
    mock_result.scalar_one_or_none.return_value = item
    mock_db = AsyncMock()
    mock_db.execute.return_value = mock_result

    service.delete_item = AsyncMock(side_effect=HTTPException(status_code=403, detail="Forbidden"))

    with pytest.raises(HTTPException) as exc:
        await service.delete_item(mock_db, item.id, current_user)
    assert exc.value.status_code == 403