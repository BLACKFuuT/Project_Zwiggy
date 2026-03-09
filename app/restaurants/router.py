from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List

from app.core.database import get_db
from app.auth.dependencies import get_current_user

from .schemas import (
    RestaurantCreate,
    RestaurantUpdate,
    RestaurantResponse,
    RestaurantListResponse
)

from .service import RestaurantService
from app.users.models import User

router = APIRouter(prefix="/restaurants", tags=["Restaurants"])

service = RestaurantService()


@router.post("/", response_model=RestaurantResponse)
async def create_restaurant(
    data: RestaurantCreate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    return await service.create_restaurant(db, data, current_user)


@router.get("/{restaurant_id}", response_model=RestaurantResponse)
async def get_restaurant(
    restaurant_id: int,
    db: AsyncSession = Depends(get_db)
):
    return await service.get_restaurant(db, restaurant_id)


@router.get("/", response_model=List[RestaurantListResponse])
async def list_restaurants(
    skip: int = 0,
    limit: int = 10,
    db: AsyncSession = Depends(get_db)
):
    return await service.list_restaurants(db, skip, limit)


@router.put("/{restaurant_id}", response_model=RestaurantResponse)
async def update_restaurant(
    restaurant_id: int,
    data: RestaurantUpdate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    return await service.update_restaurant(
        db,
        restaurant_id,
        data,
        current_user
    )


@router.delete("/{restaurant_id}")
async def delete_restaurant(
    restaurant_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    return await service.delete_restaurant(
        db,
        restaurant_id,
        current_user
    )