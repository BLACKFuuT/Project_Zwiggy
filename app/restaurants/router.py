# app/restaurants/router.py

from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List

from app.core.database import get_db
from app.auth.dependencies import get_current_user, require_permission

from .service import RestaurantService
from .schemas import (
    RestaurantCreate,
    RestaurantUpdate,
    RestaurantResponse,
    RestaurantListResponse  # <- new user-friendly schema
)

router = APIRouter(prefix="/restaurants", tags=["Restaurants"])
service = RestaurantService()


# -------------------- CRUD Endpoints --------------------

@router.post("/", response_model=RestaurantResponse)
async def create_restaurant(
    data: RestaurantCreate,
    db: AsyncSession = Depends(get_db),
    current_user = Depends(require_permission("create_restaurant")),
):
    return await service.create_restaurant(db, data, current_user)


@router.get("/{restaurant_id}", response_model=RestaurantResponse)
async def get_restaurant(
    restaurant_id: int,
    db: AsyncSession = Depends(get_db),
):
    return await service.get_restaurant(db, restaurant_id)


@router.patch("/{restaurant_id}", response_model=RestaurantResponse)
async def update_restaurant(
    restaurant_id: int,
    data: RestaurantUpdate,
    db: AsyncSession = Depends(get_db),
    current_user = Depends(require_permission("update_restaurant")),
):
    return await service.update_restaurant(
        db,
        restaurant_id,
        data,
        current_user,
    )


@router.delete("/{restaurant_id}")
async def delete_restaurant(
    restaurant_id: int,
    db: AsyncSession = Depends(get_db),
    current_user = Depends(require_permission("delete_restaurant")),
):
    await service.delete_restaurant(
        db,
        restaurant_id,
        current_user,
    )
    return {"message": "Restaurant deleted successfully"}


# -------------------- User-Friendly Endpoints --------------------

@router.get("/", response_model=List[RestaurantListResponse])
async def list_restaurants(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, le=100),
    db: AsyncSession = Depends(get_db),
):
    """
    Returns a user-friendly list of restaurants (id + name + description + address)
    for selection in frontend or API docs.
    """
    restaurants = await service.list_restaurants(db, skip, limit)
    return [
        {
            "id": r.id,
            "name": r.name,
            "description": r.description,
            "address": r.address,
        } for r in restaurants
    ]