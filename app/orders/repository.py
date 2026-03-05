from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, update
from app.orders.models import Order, OrderItem


class OrderRepository:

    async def create_order(
        self,
        db: AsyncSession,
        order: Order
    ) -> Order:
        db.add(order)
        await db.flush()
        return order

    async def create_order_item(
        self,
        db: AsyncSession,
        order_item: OrderItem
    ) -> OrderItem:
        db.add(order_item)
        await db.flush()
        return order_item

    async def get_order_by_id(
        self,
        db: AsyncSession,
        order_id: int
    ) -> Order | None:
        result = await db.execute(
            select(Order).where(
                Order.id == order_id,
                Order.deleted_at.is_(None)
            )
        )
        return result.scalar_one_or_none()

    async def update_order_total(
        self,
        db: AsyncSession,
        order_id: int,
        total: float
    ):
        await db.execute(
            update(Order)
            .where(Order.id == order_id)
            .values(total_amount=total)
        )

    async def update_status(
        self,
        db: AsyncSession,
        order_id: int,
        status: str
    ):
        await db.execute(
            update(Order)
            .where(Order.id == order_id)
            .values(status=status)
        )