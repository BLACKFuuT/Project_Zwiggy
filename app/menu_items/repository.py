from datetime import datetime
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from .models import MenuItem


class MenuItemRepository:

    async def create(self, db: AsyncSession, data: dict) -> MenuItem:
        item = MenuItem(**data)
        db.add(item)
        await db.flush()
        return item


    async def get_by_id(self, db: AsyncSession, item_id: int):
        result = await db.execute(
            select(MenuItem).where(
                MenuItem.id == item_id,
                MenuItem.deleted_at.is_(None)
            )
        )
        return result.scalar_one_or_none()


    async def list_by_restaurant(
        self,
        db: AsyncSession,
        restaurant_id: int
    ):
        result = await db.execute(
            select(MenuItem).where(
                MenuItem.restaurant_id == restaurant_id,
                MenuItem.deleted_at.is_(None)
            )
        )

        return result.scalars().all()


    async def update(
        self,
        db: AsyncSession,
        item: MenuItem,
        update_data: dict
    ):
        for field, value in update_data.items():
            setattr(item, field, value)

        await db.flush()
        return item


    async def soft_delete(
        self,
        db: AsyncSession,
        item: MenuItem
    ):
        item.deleted_at = datetime.utcnow()
        await db.flush()