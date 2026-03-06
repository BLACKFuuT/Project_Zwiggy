from fastapi import HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from sqlalchemy.orm import selectinload
from .repository import MenuItemRepository
from .schemas import MenuItemCreate, MenuItemUpdate
from app.restaurants.models import Restaurant
from app.users.models import User
from app.menu_items.models import MenuItem

class MenuItemService:
    
    def __init__(self):
        self.repository = MenuItemRepository()

    async def create_item(self, db: AsyncSession, data: MenuItemCreate, current_user: User):
        # Validate that the restaurant belongs to current user
        result = await db.execute(
            select(Restaurant).where(
                Restaurant.id == data.restaurant_id,
                Restaurant.owner_id == current_user.id
            )
        )
        restaurant = result.scalar_one_or_none()
        if not restaurant:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="You don't own this restaurant"
            )

        item = await self.repository.create(db, data.model_dump())
        await db.commit()
        await db.refresh(item)
        return item

    async def get_item(self, db: AsyncSession, item_id: int):
        item = await self.repository.get_by_id(db, item_id)
        if not item:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Menu item not found")
        return item

    async def list_items(self, db: AsyncSession, restaurant_id: int):
        return await self.repository.list_by_restaurant(db, restaurant_id)

    async def update_item(self, db: AsyncSession, item_id: int, data: MenuItemUpdate, current_user: User):
    # Fetch item with its restaurant eagerly loaded
        result = await db.execute(
            select(MenuItem)
            .options(selectinload(MenuItem.restaurant))  # eager-load restaurant
            .where(MenuItem.id == item_id)
        )
        item = result.scalar_one_or_none()

        if not item:
            raise HTTPException(status_code=404, detail="Menu item not found")

        # Verify ownership
        if item.restaurant.owner_id != current_user.id:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized")

        # Update the item
        updated_item = await self.repository.update(
            db,
            item,
            data.model_dump(exclude_unset=True)
        )
        await db.commit()
        await db.refresh(updated_item)
        return updated_item
    
    
    async def delete_item(self, db: AsyncSession, item_id: int, current_user: User):
        # Fetch item with its restaurant eagerly loaded
        result = await db.execute(
            select(MenuItem)
            .options(selectinload(MenuItem.restaurant))  # eager-load restaurant
            .where(MenuItem.id == item_id)
        )
        item = result.scalar_one_or_none()

        if not item:
            raise HTTPException(status_code=404, detail="Menu item not found")

        # Verify ownership
        if item.restaurant.owner_id != current_user.id:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized")

        # Soft delete the item
        await self.repository.soft_delete(db, item)
        await db.commit()

        return {"message": "Menu item deleted"}