from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db
from app.auth.dependencies import require_permission
from app.users.models import User

from app.payments.schemas import PaymentCreate, PaymentResponse
from app.payments.service import PaymentService

router = APIRouter(prefix="/payments", tags=["Payments"])

service = PaymentService()


@router.post(
    "/",
    response_model=PaymentResponse,
)
async def initiate_payment(
    data: PaymentCreate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(require_permission("create_payment")),
):
    return await service.initiate_payment(
        db,
        data.order_id,
        current_user,
    )


@router.post(
    "/{payment_id}/confirm",
    response_model=PaymentResponse,
)
async def confirm_payment(
    payment_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(require_permission("confirm_payment")),
):
    return await service.confirm_payment(
        db,
        payment_id,
        current_user,
    )