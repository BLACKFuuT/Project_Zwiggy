from fastapi import HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.security import verify_password, create_access_token, create_refresh_token
from app.users.repository import UserRepository


class AuthService:

    def __init__(self, db: AsyncSession):
        self.repo = UserRepository(db)

    async def login(self, email: str, password: str):

        user = await self.repo.get_by_email(email)

        if not user:
            raise HTTPException(status_code=401, detail="Invalid credentials")

        if not verify_password(password, user.hashed_password):
            raise HTTPException(status_code=401, detail="Invalid credentials")

        access_token = create_access_token(
            {"sub": str(user.id)}
        )

        refresh_token = create_refresh_token(
            {"sub": str(user.id)}
        )

        return {
            "access_token": access_token,
            "refresh_token": refresh_token,
            "token_type": "bearer"
        }