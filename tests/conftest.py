import pytest_asyncio
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from uuid import uuid4
from unittest.mock import AsyncMock, patch
from app.core.database import Base
from app.main import app
from app.auth.dependencies import get_current_user

from httpx import AsyncClient, ASGITransport
from app.main import app

DATABASE_URL = "sqlite+aiosqlite:///:memory:"

engine = create_async_engine(DATABASE_URL, future=True)

TestingSessionLocal = sessionmaker(
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False,
)


@pytest_asyncio.fixture
async def db():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    async with TestingSessionLocal() as session:
        yield session

<<<<<<< HEAD

@pytest.fixture
def mock_user():
    return type("User", (), {"id": uuid4()})()


@pytest.fixture(autouse=True)
def override_user(mock_user):
    app.dependency_overrides[get_current_user] = lambda: mock_user
    yield
    app.dependency_overrides.clear()
    
    
@pytest.fixture(autouse=True)
def mock_redis():
    with patch("app.restaurants.service.redis_client.get", new_callable=AsyncMock) as mock_get, \
         patch("app.restaurants.service.redis_client.set", new_callable=AsyncMock), \
         patch("app.restaurants.service.redis_client.delete", new_callable=AsyncMock):

        mock_get.return_value = None
        yield




@pytest.fixture
async def client():
    transport = ASGITransport(app=app)

    async with AsyncClient(
        transport=transport,
        base_url="http://test"
    ) as ac:
        yield ac
=======
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
>>>>>>> aashish-users-module
