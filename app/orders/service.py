from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import HTTPException
from app.orders.repository import OrderRepository
from app.orders.models import Order, OrderItem
from app.orders.schemas import OrderCreate
from app.restaurants.models import Restaurant
from sqlalchemy import select


class OrderService:

    def __init__(self):
        self.repository = OrderRepository()

    async def create_order(
        self,
        db: AsyncSession,
        data: OrderCreate,
        customer_id: int
    ):

        # 1️⃣ Validate restaurant exists
        restaurant = await db.execute(
            select(Restaurant).where(
                Restaurant.id == data.restaurant_id,
                Restaurant.deleted_at.is_(None)
            )
        )
        restaurant = restaurant.scalar_one_or_none()

        if not restaurant:
            raise HTTPException(status_code=404, detail="Restaurant not found")

        # 2️⃣ Create Order
        order = Order(
            customer_id=customer_id,
            restaurant_id=data.restaurant_id,
            status="PENDING"
        )

        await self.repository.create_order(db, order)

        total_amount = 0

        # 3️⃣ Create Order Items
        for item in data.items:

            # 🔥 For now assume price = 100
            # Later fetch from MenuItem table
            price = 100

            order_item = OrderItem(
                order_id=order.id,
                menu_item_id=item.menu_item_id,
                quantity=item.quantity,
                price=price
            )

            await self.repository.create_order_item(db, order_item)

            total_amount += price * item.quantity

        # 4️⃣ Update total
        await self.repository.update_order_total(
            db,
            order.id,
            total_amount
        )

        # 5️⃣ Commit transaction
        await db.commit()

        # 6️⃣ Refresh order
        await db.refresh(order)

        return order

    async def get_order(
        self,
        db: AsyncSession,
        order_id: int,
        current_user_id: int
    ):
        order = await self.repository.get_order_by_id(db, order_id)

        if not order:
            raise HTTPException(status_code=404, detail="Order not found")

        # RBAC: only owner can view
        if order.customer_id != current_user_id:
            raise HTTPException(status_code=403, detail="Forbidden")

        return order