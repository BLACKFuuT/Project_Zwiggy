# app/restaurants/router.py

from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db
# from auth.dependencies import get_current_user

from .service import RestaurantService
from .schemas import (
    RestaurantCreate,
    RestaurantUpdate,
    RestaurantResponse
)

router = APIRouter(prefix="/restaurants", tags=["Restaurants"])

service = RestaurantService()


@router.post("/", response_model=RestaurantResponse)
async def create_restaurant(
    data: RestaurantCreate,
    db: AsyncSession = Depends(get_db),
    # current_user = Depends(get_current_user)
):
    return await service.create_restaurant(
        db,
        data,
        # owner_id=current_user.id
    )


@router.get("/{restaurant_id}", response_model=RestaurantResponse)
async def get_restaurant(
    restaurant_id: int,
    db: AsyncSession = Depends(get_db)
):
    return await service.get_restaurant(db, restaurant_id)


@router.get("/", response_model=list[RestaurantResponse])
async def list_restaurants(
    skip: int = Query(0, ge=0),
    limit: int = Query(10, le=100),
    db: AsyncSession = Depends(get_db)
):
    return await service.list_restaurants(db, skip, limit)


@router.patch("/{restaurant_id}", response_model=RestaurantResponse)
async def update_restaurant(
    restaurant_id: int,
    data: RestaurantUpdate,
    db: AsyncSession = Depends(get_db),
    # current_user = Depends(get_current_user)
):
    return await service.update_restaurant(
        db,
        restaurant_id,
        data,
        # current_user.id
    )


@router.delete("/{restaurant_id}")
async def delete_restaurant(
    restaurant_id: int,
    db: AsyncSession = Depends(get_db),
    # current_user = Depends(get_current_user)
):
    await service.delete_restaurant(
        db,
        restaurant_id,
        # current_user.id
    )
    return {"message": "Restaurant deleted successfully"}