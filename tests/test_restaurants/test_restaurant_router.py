import pytest
from httpx import AsyncClient
from unittest.mock import AsyncMock, patch
from uuid import uuid4

from app.main import app


from datetime import datetime
from uuid import uuid4
@pytest.mark.asyncio
async def test_create_restaurant(client):

    payload = {
        "name": "Pizza Hut",
        "description": "Best pizza",
        "address": "Delhi"
    }

    fake_response = {
    "id": 1,
    "name": "Pizza Hut",
    "description": None,
    "address": "Mumbai",
    "owner_id": str(uuid4()),
    "is_active": True,
    "created_at": datetime.utcnow().isoformat(),
    "updated_at": datetime.utcnow().isoformat()
}

    with patch(
        "app.restaurants.router.service.create_restaurant",
        new_callable=AsyncMock
    ) as mock_service:

        mock_service.return_value = fake_response

        response = await client.post("/restaurants/", json=payload)

        assert response.status_code == 200
        assert response.json()["name"] == "Pizza Hut"
        

@pytest.mark.asyncio
async def test_get_restaurant(client):

    fake_response = {
    "id": 1,
    "name": "Dominos",
    "description": None,
    "address": "Mumbai",
    "owner_id": str(uuid4()),
    "is_active": True,
    "created_at": datetime.utcnow().isoformat(),
    "updated_at": datetime.utcnow().isoformat()
}

    with patch(
        "app.restaurants.router.service.get_restaurant",
        new_callable=AsyncMock
    ) as mock_service:

        mock_service.return_value = fake_response

        response = await client.get("/restaurants/1")

        assert response.status_code == 200
        assert response.json()["name"] == "Dominos"
        
        
@pytest.mark.asyncio
async def test_list_restaurants(client):

    fake_list = [
        {
            "id": 1,
            "name": "Pizza Hut",
            "address": "Delhi"
        },
        {
            "id": 2,
            "name": "Dominos",
            "address": "Mumbai"
        }
    ]

    with patch(
        "app.restaurants.router.service.list_restaurants",
        new_callable=AsyncMock
    ) as mock_service:

        mock_service.return_value = fake_list

        response = await client.get("/restaurants/")

        assert response.status_code == 200
        assert len(response.json()) == 2
        
        
@pytest.mark.asyncio
async def test_update_restaurant(client):

    payload = {"name": "Updated Restaurant"}

    fake_response = {
    "id": 1,
    "name": "Updated Restaurant",
    "address": "Delhi",
    "owner_id": str(uuid4()),
    "is_active": True,
    "created_at": datetime.utcnow().isoformat(),
    "updated_at": datetime.utcnow().isoformat()
}

    with patch(
        "app.restaurants.router.service.update_restaurant",
        new_callable=AsyncMock
    ) as mock_service:

        mock_service.return_value = fake_response

        response = await client.put("/restaurants/1", json=payload)

        assert response.status_code == 200
        assert response.json()["name"] == "Updated Restaurant"
        
        
        
@pytest.mark.asyncio
async def test_delete_restaurant(client):

    fake_response = {"message": "Restaurant deleted successfully"}

    with patch(
        "app.restaurants.router.service.delete_restaurant",
        new_callable=AsyncMock
    ) as mock_service:

        mock_service.return_value = fake_response

        response = await client.delete("/restaurants/1")

        assert response.status_code == 200
        assert response.json()["message"] == "Restaurant deleted successfully"