import uuid
from fastapi import HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.payments.repository import PaymentRepository
from app.orders.repository import OrderRepository
from app.payments.models import Payment
from app.users.models import User


class PaymentService:

    def __init__(self):
        self.repository = PaymentRepository()
        self.order_repo = OrderRepository()

    async def initiate_payment(
        self,
        db: AsyncSession,
        order_id: int,
        current_user: User
    ):

        # 1️⃣ Validate order
        order = await self.order_repo.get_order_by_id(db, order_id)

        if not order:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Order not found"
            )

        # 2️⃣ Ensure user owns the order
        if order.customer_id != current_user.id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Forbidden"
            )

        # 3️⃣ Prevent duplicate payments
        existing = await self.repository.get_by_order_id(
            db,
            order_id
        )

        if existing:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Payment already initiated for this order"
            )

        # 4️⃣ Create payment
        payment = Payment(
            order_id=order.id,
            amount=order.total_amount,
            status="INITIATED",
        )

        await self.repository.create(db, payment)

        await db.commit()
        await db.refresh(payment)

        return payment

    async def confirm_payment(
        self,
        db: AsyncSession,
        payment_id: int,
        current_user: User
    ):

        payment = await self.repository.get_by_id(
            db,
            payment_id
        )

        if not payment:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Payment not found"
            )

        # simulate payment gateway success
        transaction_id = str(uuid.uuid4())

        await self.repository.update_status(
            db,
            payment_id,
            status="SUCCESS",
            transaction_id=transaction_id,
        )

        # update order status
        await self.order_repo.update_status(
            db,
            payment.order_id,
            "CONFIRMED"
        )

        await db.commit()

        updated_payment = await self.repository.get_by_id(
            db,
            payment_id
        )

        return updated_payment  