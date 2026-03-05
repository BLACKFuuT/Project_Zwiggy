from fastapi import HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from .repository import MenuItemRepository
from .schemas import MenuItemCreate, MenuItemUpdate


class MenuItemService:

    def __init__(self):
        self.repository = MenuItemRepository()

    async def create_item(self, db: AsyncSession, data: MenuItemCreate):
        return await self.repository.create(db, data.model_dump())

    async def get_item(self, db: AsyncSession, item_id: int):
        item = await self.repository.get_by_id(db, item_id)

        if not item:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Menu item not found"
            )

        return item

    async def list_items(self, db: AsyncSession, restaurant_id: int):
        return await self.repository.list_by_restaurant(db, restaurant_id)

    async def update_item(self, db: AsyncSession, item_id: int, data: MenuItemUpdate):
        item = await self.get_item(db, item_id)

        return await self.repository.update(
            db, item, data.model_dump(exclude_unset=True)
        )

    async def delete_item(self, db: AsyncSession, item_id: int):
        item = await self.get_item(db, item_id)

        await self.repository.soft_delete(db, item)
