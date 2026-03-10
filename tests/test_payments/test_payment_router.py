import pytest
from fastapi import FastAPI
from httpx import AsyncClient, ASGITransport
from unittest.mock import AsyncMock, patch

from app.payments.router import router
from app.core.database import get_db
from app.users.models import User


@pytest.fixture
def fake_user():
    return User(id=1, email="test@test.com")


@pytest.fixture
def app(fake_user):
    app = FastAPI()
    app.include_router(router)

    async def fake_db():
        yield AsyncMock()

    async def fake_permission():
        return fake_user

    app.dependency_overrides[get_db] = fake_db

    # override permission dependency
    for route in router.routes:
        for dep in route.dependant.dependencies:
            if "require_permission" in str(dep.call):
                app.dependency_overrides[dep.call] = fake_permission

    return app


@pytest.mark.asyncio
async def test_initiate_payment(app):

    with patch(
        "app.payments.service.PaymentService.initiate_payment",
        new_callable=AsyncMock
    ) as mock_initiate:

        mock_initiate.return_value = {
            "id": 1,
            "order_id": 10,
            "amount": 100,
            "provider": "stripe",
            "transaction_id": "txn_123",
            "status": "pending",
            "created_at": "2024-01-01T00:00:00"
        }

        transport = ASGITransport(app=app)

        async with AsyncClient(transport=transport, base_url="http://test") as client:
            response = await client.post(
                "/payments/",
                json={"order_id": 10}
            )

        assert response.status_code == 200
        assert response.json()["status"] == "pending"


@pytest.mark.asyncio
async def test_confirm_payment(app):

    with patch(
        "app.payments.service.PaymentService.confirm_payment",
        new_callable=AsyncMock
    ) as mock_confirm:

        mock_confirm.return_value = {
            "id": 1,
            "order_id": 10,
            "amount": 100,
            "provider": "stripe",
            "transaction_id": "txn_123",
            "status": "success",
            "created_at": "2024-01-01T00:00:00"
        }

        transport = ASGITransport(app=app)

        async with AsyncClient(transport=transport, base_url="http://test") as client:
            response = await client.post("/payments/1/confirm")

        assert response.status_code == 200
        assert response.json()["status"] == "success"