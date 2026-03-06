from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import HTTPException, status

from .repository import RestaurantRepository
from .schemas import RestaurantCreate, RestaurantUpdate
from app.users.models import User


class RestaurantService:

    def __init__(self):
        self.repository = RestaurantRepository()

    async def create_restaurant(
        self,
        db: AsyncSession,
        data: RestaurantCreate,
        current_user: User
    ):
        restaurant = await self.repository.create(
            db,
            {**data.model_dump(), "owner_id": current_user.id}
        )

        await db.commit()
        await db.refresh(restaurant)

        return restaurant


    async def get_restaurant(
        self,
        db: AsyncSession,
        restaurant_id: int
    ):
        restaurant = await self.repository.get_by_id(db, restaurant_id)

        if not restaurant:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Restaurant not found"
            )

        return restaurant


    async def list_restaurants(
        self,
        db: AsyncSession,
        skip: int = 0,
        limit: int = 10
    ):
        return await self.repository.list(db, skip, limit)


    async def update_restaurant(
        self,
        db: AsyncSession,
        restaurant_id: int,
        data: RestaurantUpdate,
        current_user: User
    ):
        restaurant = await self.get_restaurant(db, restaurant_id)

        if restaurant.owner_id != current_user.id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Not allowed to update this restaurant"
            )

        updated_restaurant = await self.repository.update(
            db,
            restaurant,
            data.model_dump(exclude_unset=True)
        )

        await db.commit()
        await db.refresh(updated_restaurant)

        return updated_restaurant


    async def delete_restaurant(
        self,
        db: AsyncSession,
        restaurant_id: int,
        current_user: User
    ):
        restaurant = await self.get_restaurant(db, restaurant_id)

        if restaurant.owner_id != current_user.id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Not allowed to delete this restaurant"
            )

        await self.repository.soft_delete(db, restaurant)

        await db.commit()
        await db.refresh(restaurant)

        return {"message": "Restaurant deleted successfully"}