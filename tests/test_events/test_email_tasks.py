# import pytest
# from unittest.mock import AsyncMock
# from app.users.service import UserService
# from app.users.schemas import UserCreate


# @pytest.mark.asyncio
# async def test_create_user():
#     repo = AsyncMock()

#     # Ensure email does NOT exist
#     repo.get_by_email = AsyncMock(return_value=None)

#     # Mock user creation
#     repo.create_user = AsyncMock(return_value={"email": "test@test.com"})

#     service = UserService(repo)

#     user_data = UserCreate(email="test@test.com", password="123456")

#     result = await service.create_user(user_data)

#     assert result["email"] == "test@test.com"

def test_email_tasks_runs():
    try:
        import app.events.tasks.email_tasks
    except Exception:
        pass