from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.database import get_db
from app.orders.schemas import OrderCreate, OrderResponse
from app.orders.service import OrderService
from app.auth.dependencies import get_current_user

router = APIRouter(prefix="/orders", tags=["Orders"])

service = OrderService()


@router.post("/", response_model=OrderResponse)
async def create_order(
    data: OrderCreate,
    db: AsyncSession = Depends(get_db),
    current_user=Depends(get_current_user)
):
    return await service.create_order(
        db,
        data,
        customer_id=current_user.id
    )


@router.get("/{order_id}", response_model=OrderResponse)
async def get_order(
    order_id: int,
    db: AsyncSession = Depends(get_db),
    current_user=Depends(get_current_user)
):
    return await service.get_order(
        db,
        order_id,
        current_user.id
    )