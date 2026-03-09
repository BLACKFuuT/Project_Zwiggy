import pytest
from unittest.mock import AsyncMock, patch
from fastapi import HTTPException
from app.users.service import UserService
from app.users.schemas import UserCreate
from app.users.models import User, Profile

@pytest.mark.asyncio
async def test_create_user():
    # Mock the AsyncSession
    db_mock = AsyncMock()

    service = UserService(db_mock)

    # Patch repository methods inside the service
    service.repo.get_by_email = AsyncMock(return_value=None)
    service.repo.create_user = AsyncMock(
        return_value=User(
            email="test@test.com",
            hashed_password="hashed",
            profile=Profile(address="addr", phone="123456")
        )
    )

    # Patch RBACRepository methods
    with patch("app.users.service.RBACRepository") as rbac_mock_class:
        rbac_mock = rbac_mock_class.return_value
        rbac_mock.get_role_by_name = AsyncMock(return_value=type("Role", (), {"id": 1})())
        rbac_mock.assign_role = AsyncMock(return_value=None)

        user_data = UserCreate(
            email="test@test.com",
            password="123456",
            address="addr",
            phone="123456"
        )

        user = await service.create_user(user_data)

        assert user.email == "test@test.com"
        assert user.profile.phone == "123456"
        service.repo.get_by_email.assert_awaited_once_with("test@test.com")
        service.repo.create_user.assert_awaited_once()
        rbac_mock.get_role_by_name.assert_awaited_once_with("Customer")
        rbac_mock.assign_role.assert_awaited_once() 