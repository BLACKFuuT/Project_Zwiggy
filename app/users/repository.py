# modules/users/repository.py

from typing import Optional
from uuid import UUID

from sqlalchemy import select, update
from sqlalchemy.ext.asyncio import AsyncSession

from .models import User, Profile


class UserRepository:

    def __init__(self, db: AsyncSession):
        self.db = db

    async def create_user(self, user: User) -> User:
        self.db.add(user)
        await self.db.flush()
        await self.db.refresh(user)
        return user

    async def get_by_email(self, email: str) -> Optional[User]:
        stmt = select(User).where(
            User.email == email,
            User.deleted_at.is_(None),
        )
        result = await self.db.execute(stmt)
        return result.scalar_one_or_none()

    async def get_by_id(self, user_id: UUID) -> Optional[User]:
        stmt = select(User).where(
            User.id == user_id,
            User.deleted_at.is_(None),
        )
        result = await self.db.execute(stmt)
        return result.scalar_one_or_none()

    async def soft_delete(self, user: User):
        from datetime import datetime
        user.deleted_at = datetime.utcnow()
        await self.db.flush()