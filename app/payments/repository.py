from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, update
from app.payments.models import Payment


class PaymentRepository:

    async def create(
        self,
        db: AsyncSession,
        payment: Payment
    ) -> Payment:
        db.add(payment)
        await db.flush()
        return payment

    async def get_by_id(
        self,
        db: AsyncSession,
        payment_id: int
    ) -> Payment | None:
        result = await db.execute(
            select(Payment).where(Payment.id == payment_id)
        )
        return result.scalar_one_or_none()

    async def update_status(
        self,
        db: AsyncSession,
        payment_id: int,
        status: str,
        transaction_id: str | None = None
    ):
        await db.execute(
            update(Payment)
            .where(Payment.id == payment_id)
            .values(
                status=status,
                transaction_id=transaction_id
            )
        )
        
    async def get_by_order_id(
        self,
        db: AsyncSession,
        order_id: int
    ):
        result = await db.execute(
            select(Payment).where(Payment.order_id == order_id)
        )
        return result.scalar_one_or_none()