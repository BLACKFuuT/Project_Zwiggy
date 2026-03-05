# app/restaurants/repository.py

from datetime import datetime
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from .models import Restaurant


class RestaurantRepository:

    async def create(self, db: AsyncSession, data: dict) -> Restaurant:
        restaurant = Restaurant(**data)
        db.add(restaurant)
        await db.flush()
        return restaurant

    async def get_by_id(
        self, db: AsyncSession, restaurant_id: int
    ) -> Restaurant | None:
        result = await db.execute(
            select(Restaurant).where(
                Restaurant.id == restaurant_id, Restaurant.deleted_at.is_(None)
            )
        )
        return result.scalar_one_or_none()

    async def list(self, db: AsyncSession, skip: int = 0, limit: int = 10):
        result = await db.execute(
            select(Restaurant)
            .where(Restaurant.deleted_at.is_(None))
            .offset(skip)
            .limit(limit)
        )
        return result.scalars().all()

    async def update(self, db: AsyncSession, restaurant: Restaurant, update_data: dict):
        for field, value in update_data.items():
            setattr(restaurant, field, value)

        await db.flush()
        return restaurant

    async def soft_delete(self, db: AsyncSession, restaurant: Restaurant):
        restaurant.deleted_at = datetime.utcnow()
        await db.flush()
