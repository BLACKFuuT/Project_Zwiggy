import uuid
from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.payments.repository import PaymentRepository
from app.payments.models import Payment
from app.orders.models import Order


class PaymentService:

    def __init__(self):
        self.repository = PaymentRepository()

    async def initiate_payment(
        self,
        db: AsyncSession,
        order_id: int,
        user_id: int
    ):

        # 1️⃣ Validate order exists
        result = await db.execute(
            select(Order).where(Order.id == order_id)
        )
        order = result.scalar_one_or_none()

        if not order:
            raise HTTPException(404, "Order not found")

        if order.customer_id != user_id:
            raise HTTPException(403, "Forbidden")

        if order.status != "PENDING":
            raise HTTPException(400, "Order already processed")

        # 2️⃣ Create payment record
        payment = Payment(
            order_id=order.id,
            amount=order.total_amount,
            status="INITIATED"
        )

        await self.repository.create(db, payment)
        await db.commit()
        await db.refresh(payment)

        return payment

    async def confirm_payment(
        self,
        db: AsyncSession,
        payment_id: int
    ):

        payment = await self.repository.get_by_id(db, payment_id)

        if not payment:
            raise HTTPException(404, "Payment not found")

        # 🔥 Simulate payment success
        transaction_id = str(uuid.uuid4())

        await self.repository.update_status(
            db,
            payment_id,
            status="SUCCESS",
            transaction_id=transaction_id
        )

        # Update order status
        await db.execute(
            select(Order).where(Order.id == payment.order_id)
        )

        await db.execute(
            Order.__table__.update()
            .where(Order.id == payment.order_id)
            .values(status="CONFIRMED")
        )

        await db.commit()

        return payment