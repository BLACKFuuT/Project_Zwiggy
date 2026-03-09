import pytest
from uuid import uuid4

from app.restaurants.repository import RestaurantRepository
from app.restaurants.models import Restaurant


@pytest.mark.asyncio
async def test_create_restaurant(db):
    repo = RestaurantRepository()

    data = {
        "name": "Pizza Hut",
        "description": "Best pizza",
        "address": "Delhi",
        "owner_id": uuid4()
    }

    restaurant = await repo.create(db, data)

    assert isinstance(restaurant, Restaurant)
    assert restaurant.name == "Pizza Hut"
    assert restaurant.address == "Delhi"
    
    
@pytest.mark.asyncio
async def test_get_restaurant_by_id(db):
    repo = RestaurantRepository()

    data = {
        "name": "Dominos",
        "address": "Mumbai",
        "owner_id": uuid4()
    }

    restaurant = await repo.create(db, data)
    await db.commit()

    found = await repo.get_by_id(db, restaurant.id)

    assert found is not None
    assert found.id == restaurant.id
    
    
@pytest.mark.asyncio
async def test_list_restaurants(db):
    repo = RestaurantRepository()

    for i in range(3):
        data = {
            "name": f"Restaurant {i}",
            "address": "City",
            "owner_id": uuid4()
        }
        await repo.create(db, data)

    await db.commit()

    restaurants = await repo.list(db)

    assert len(restaurants) >= 3
    
    
@pytest.mark.asyncio
async def test_update_restaurant(db):
    repo = RestaurantRepository()

    data = {
        "name": "Old Name",
        "address": "Delhi",
        "owner_id": uuid4()
    }

    restaurant = await repo.create(db, data)

    update_data = {"name": "New Name"}

    updated = await repo.update(db, restaurant, update_data)

    assert updated.name == "New Name"   
    
    
@pytest.mark.asyncio
async def test_soft_delete_restaurant(db):
    repo = RestaurantRepository()

    data = {
        "name": "Delete Me",
        "address": "Delhi",
        "owner_id": uuid4()
    }

    restaurant = await repo.create(db, data)

    await repo.soft_delete(db, restaurant)

    assert restaurant.deleted_at is not None
    
    
@pytest.mark.asyncio
async def test_soft_deleted_restaurant_not_returned(db):
    repo = RestaurantRepository()

    data = {
        "name": "Hidden Restaurant",
        "address": "Delhi",
        "owner_id": uuid4()
    }

    restaurant = await repo.create(db, data)
    await repo.soft_delete(db, restaurant)
    await db.commit()

    result = await repo.get_by_id(db, restaurant.id)

    assert result is None