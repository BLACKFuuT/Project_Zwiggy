import pytest
from unittest.mock import AsyncMock, Mock, MagicMock
from datetime import datetime
from app.menu_items.repository import MenuItemRepository
from app.menu_items.models import MenuItem


@pytest.fixture
def repo():
    return MenuItemRepository()


@pytest.fixture
def mock_db():
    return AsyncMock()


@pytest.mark.asyncio
async def test_get_by_id(repo):
    item = MenuItem(
        id=1,
        name="Burger",
        description="Tasty",
        price=9.99,
        is_available=True,
        restaurant_id=1,
    )

    # Mock the Result object (scalar_one_or_none is synchronous)
    mock_result = Mock()
    mock_result.scalar_one_or_none.return_value = item

    # Mock AsyncSession
    mock_db = AsyncMock()
    mock_db.execute.return_value = mock_result  # db.execute is async, returns awaitable Result

    result = await repo.get_by_id(mock_db, 1)
    assert result == item

@pytest.mark.asyncio
async def test_list_by_restaurant(repo, mock_db):
    item1 = MenuItem(
        id=1,
        name="Burger",
        description="Tasty",
        price=9.99,
        is_available=True,
        restaurant_id=1,
    )
    item2 = MenuItem(
        id=2,
        name="Pizza",
        description="Cheesy",
        price=12.99,
        is_available=True,
        restaurant_id=1,
    )

    mock_scalars = MagicMock()
    mock_scalars.all = MagicMock(return_value=[item1, item2])

    mock_result = MagicMock()
    mock_result.scalars = MagicMock(return_value=mock_scalars)

    mock_db.execute.return_value = mock_result

    result = await repo.list_by_restaurant(mock_db, 1)
    assert result == [item1, item2]


@pytest.mark.asyncio
async def test_create(repo, mock_db):
    data = {
        "name": "Burger",
        "description": "Tasty",
        "price": 9.99,
        "is_available": True,
        "restaurant_id": 1,
    }

    # mock db.add and db.flush
    mock_db.add = MagicMock()
    mock_db.flush = AsyncMock()

    item = await repo.create(mock_db, data)
    assert item.name == "Burger"
    mock_db.add.assert_called_once_with(item)
    mock_db.flush.assert_awaited_once()


@pytest.mark.asyncio
async def test_update(repo, mock_db):
    item = MenuItem(
        id=1,
        name="Burger",
        description="Tasty",
        price=9.99,
        is_available=True,
        restaurant_id=1,
    )

    mock_db.flush = AsyncMock()
    updated_item = await repo.update(mock_db, item, {"name": "Cheeseburger"})
    assert updated_item.name == "Cheeseburger"
    mock_db.flush.assert_awaited_once()


@pytest.mark.asyncio
async def test_soft_delete(repo, mock_db):
    item = MenuItem(
        id=1,
        name="Burger",
        description="Tasty",
        price=9.99,
        is_available=True,
        restaurant_id=1,
    )

    mock_db.flush = AsyncMock()
    await repo.soft_delete(mock_db, item)
    assert isinstance(item.deleted_at, datetime)
    mock_db.flush.assert_awaited_once()
