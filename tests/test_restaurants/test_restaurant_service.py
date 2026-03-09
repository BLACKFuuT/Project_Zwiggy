import pytest
from uuid import uuid4
from unittest.mock import AsyncMock, patch

from app.restaurants.service import RestaurantService
from app.restaurants.schemas import RestaurantCreate


@pytest.mark.asyncio
async def test_create_restaurant(db):

    service = RestaurantService()

    user = type("User", (), {"id": uuid4()})()

    data = RestaurantCreate(
        name="Pizza Hut",
        description="Best pizza",
        address="Delhi"
    )

    with patch("app.restaurants.service.redis_client.delete", new_callable=AsyncMock):

        restaurant = await service.create_restaurant(db, data, user)

        assert restaurant.name == "Pizza Hut"
        assert restaurant.owner_id == user.id
        
        
@pytest.mark.asyncio
async def test_get_restaurant_cache_miss(db):

    service = RestaurantService()

    with patch("app.restaurants.service.redis_client.get", new_callable=AsyncMock) as mock_get, \
         patch("app.restaurants.service.redis_client.set", new_callable=AsyncMock):

        mock_get.return_value = None

        repo = service.repository

        restaurant = await repo.create(db, {
            "name": "Dominos",
            "address": "Mumbai",
            "owner_id": uuid4()
        })

        await db.commit()

        result = await service.get_restaurant(db, restaurant.id)

        assert result.id == restaurant.id
        
        
from fastapi import HTTPException


@pytest.mark.asyncio
async def test_get_restaurant_not_found(db):

    service = RestaurantService()

    with patch("app.restaurants.service.redis_client.get", new_callable=AsyncMock) as mock_get:
        mock_get.return_value = None

        with pytest.raises(HTTPException) as exc:

            await service.get_restaurant(db, 999)

        assert exc.value.status_code == 404
        
        
if restaurants.owner_id != current_user.id:
    raise 403