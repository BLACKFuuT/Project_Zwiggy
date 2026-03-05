from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db

from .service import MenuItemService
from .schemas import MenuItemCreate, MenuItemUpdate, MenuItemResponse

router = APIRouter(prefix="/menu-items", tags=["Menu Items"])

service = MenuItemService()


@router.post("/", response_model=MenuItemResponse)

async def create_menu_item(data: MenuItemCreate, db: AsyncSession = Depends(get_db)):
    return await service.create_item(db, data)


@router.get("/{item_id}", response_model=MenuItemResponse)
async def get_menu_item(item_id: int, db: AsyncSession = Depends(get_db)):
    return await service.get_item(db, item_id)


@router.get("/restaurant/{restaurant_id}", response_model=list[MenuItemResponse])
async def list_restaurant_menu(restaurant_id: int, db: AsyncSession = Depends(get_db)):
    return await service.list_items(db, restaurant_id)


@router.patch("/{item_id}", response_model=MenuItemResponse)
async def update_menu_item(
    item_id: int, data: MenuItemUpdate, db: AsyncSession = Depends(get_db)
):
    return await service.update_item(db, item_id, data)


@router.delete("/{item_id}")
async def delete_menu_item(item_id: int, db: AsyncSession = Depends(get_db)):
    await service.delete_item(db, item_id)

    return {"message": "Menu item deleted"}
