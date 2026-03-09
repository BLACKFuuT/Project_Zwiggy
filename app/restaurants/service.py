import json
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import HTTPException, status

from .repository import RestaurantRepository
from .schemas import RestaurantCreate, RestaurantUpdate, RestaurantResponse, RestaurantListResponse
from app.users.models import User
from app.core.redis import redis_client


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

        # clear cached list
        await redis_client.delete("restaurants:list")

        return restaurant

    async def get_restaurant(
        self,
        db: AsyncSession,
        restaurant_id: int
    ):

        cache_key = f"restaurant:{restaurant_id}"

        cached = await redis_client.get(cache_key)
        if cached:
            return RestaurantResponse(**json.loads(cached))

        restaurant = await self.repository.get_by_id(db, restaurant_id)

        if not restaurant:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Restaurant not found"
            )

        restaurant_data = RestaurantResponse.model_validate(restaurant)

        await redis_client.set(
            cache_key,
            json.dumps(restaurant_data.model_dump(), default=str),
            ex=300
        )

        return restaurant

    async def list_restaurants(
        self,
        db: AsyncSession,
        skip: int = 0,
        limit: int = 10
    ):

        cache_key = f"restaurants:list:{skip}:{limit}"

        cached = await redis_client.get(cache_key)
        if cached:
            return [RestaurantListResponse(**item) for item in json.loads(cached)]

        restaurants = await self.repository.list(db, skip, limit)

        data = [
            RestaurantListResponse.model_validate(r).model_dump()
            for r in restaurants
        ]

        await redis_client.set(
            cache_key,
            json.dumps(data, default=str),
            ex=300
        )

        return restaurants

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

        # invalidate cache
        await redis_client.delete(f"restaurant:{restaurant_id}")
        await redis_client.delete("restaurants:list")

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

        # invalidate cache
        await redis_client.delete(f"restaurant:{restaurant_id}")
        await redis_client.delete("restaurants:list")

        return {"message": "Restaurant deleted successfully"}