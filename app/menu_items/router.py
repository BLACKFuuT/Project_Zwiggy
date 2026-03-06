# app/menu_items/router.py

from fastapi import APIRouter, Depends, Form, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Optional, List

from app.core.database import get_db
from app.auth.dependencies import require_permission
from app.users.models import User

from .service import MenuItemService
from .schemas import (
    MenuItemCreate,
    MenuItemUpdate,
    MenuItemResponse,
    MenuItemListResponse,  # <- new simplified schema for listing
)

router = APIRouter(prefix="/menu-items", tags=["Menu Items"])
service = MenuItemService()


# -------------------- CRUD Endpoints --------------------

@router.post("/", response_model=MenuItemResponse)
async def create_menu_item(
    name: str = Form(...),
    description: Optional[str] = Form(None),
    price: float = Form(...),
    is_available: bool = Form(True),
    restaurant_id: int = Form(...),  # selected by owner
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(require_permission("create_menu_item")),
):
    data = MenuItemCreate(
        name=name,
        description=description,
        price=price,
        is_available=is_available,
        restaurant_id=restaurant_id
    )
    return await service.create_item(db, data, current_user)


@router.get("/{item_id}", response_model=MenuItemResponse)
async def get_menu_item(item_id: int, db: AsyncSession = Depends(get_db)):
    return await service.get_item(db, item_id)


@router.patch("/{item_id}", response_model=MenuItemResponse)
async def update_menu_item(
    item_id: int,
    data: MenuItemUpdate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(require_permission("update_menu_item")),
):
    return await service.update_item(db, item_id, data, current_user)


@router.delete("/{item_id}")
async def delete_menu_item(
    item_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(require_permission("delete_menu_item")),
):
    return await service.delete_item(db, item_id, current_user)


# -------------------- User-Friendly Endpoints --------------------

@router.get("/restaurant/{restaurant_id}", response_model=List[MenuItemListResponse])
async def list_restaurant_menu(
    restaurant_id: int,
    db: AsyncSession = Depends(get_db),
):
    """
    Returns a user-friendly menu list for a given restaurant:
    Includes id, name, price, availability
    """
    items = await service.list_items(db, restaurant_id)
    if not items:
        raise HTTPException(status_code=404, detail="No menu items found for this restaurant")
    return [
        {
            "id": item.id,
            "name": item.name,
            "price": float(item.price),
            "is_available": item.is_available
        }
        for item in items
    ]