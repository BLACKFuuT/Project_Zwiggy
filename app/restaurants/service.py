# app/restaurants/service.py

from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import HTTPException, status

from .repository import RestaurantRepository
from .schemas import RestaurantCreate, RestaurantUpdate


class RestaurantService:

    def __init__(self):
        self.repository = RestaurantRepository()


    async def create_restaurant(
        self,
        db: AsyncSession,
        data: RestaurantCreate,
        # owner_id: int
    ):
        restaurant = await self.repository.create(db,{**data.model_dump()}
            # {**data.model_dump(), "owner_id": owner_id}
            
        )
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
        skip: int,
        limit: int
    ):
        return await self.repository.list(db, skip, limit)


    async def update_restaurant(
        self,
        db: AsyncSession,
        restaurant_id: int,
        data: RestaurantUpdate,
        # current_user_id: int
    ):
        restaurant = await self.get_restaurant(db, restaurant_id)

        # if restaurant.owner_id != current_user_id:
        #     raise HTTPException(
        #         status_code=status.HTTP_403_FORBIDDEN,
        #         detail="Not allowed"
        #     )

        return await self.repository.update(
            db,
            restaurant,
            data.model_dump(exclude_unset=True)
        )


    async def delete_restaurant(
        self,
        db: AsyncSession,
        restaurant_id: int,
        # current_user_id: int
    ):
        restaurant = await self.get_restaurant(db, restaurant_id)

        # if restaurant.owner_id != current_user_id:
        #     raise HTTPException(
        #         status_code=status.HTTP_403_FORBIDDEN,
        #         detail="Not allowed"
        #     )

        await self.repository.soft_delete(db, restaurant)