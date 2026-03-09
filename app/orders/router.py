from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List
from sqlalchemy.orm import selectinload
from sqlalchemy import select

from app.core.database import get_db
from app.auth.dependencies import require_permission
from app.users.models import User
from app.orders.models import Order, OrderItem
from app.menu_items.repository import MenuItemRepository
from .schemas import OrderCreate, OrderResponse, OrderItemResponse
from .service import OrderService

router = APIRouter(prefix="/orders", tags=["Orders"])
service = OrderService()
menu_repo = MenuItemRepository()


@router.post("/", response_model=OrderResponse)
async def create_order(
    data: OrderCreate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(require_permission("create_order"))
):
    order = await service.create_order(db, data, current_user)

    items_response: List[OrderItemResponse] = [
        OrderItemResponse(
            menu_item_id=item.menu_item_id,
            menu_item_name=(await menu_repo.get_by_id(db, item.menu_item_id)).name,
            quantity=item.quantity,
            price=float(item.price)
        )
        for item in order.items
    ]

    return OrderResponse(
        id=order.id,
        customer_id=order.customer_id,
        restaurant_id=order.restaurant_id,
        restaurant_name=order.restaurant.name,
        status=order.status,
        total_amount=float(order.total_amount),
        created_at=order.created_at,
        items=items_response
    )


@router.get("/{order_id}", response_model=OrderResponse)
async def get_order(
    order_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(require_permission("view_order"))
):
    order = await service.get_order(db, order_id, current_user)

    items_response: List[OrderItemResponse] = [
        OrderItemResponse(
            menu_item_id=item.menu_item_id,
            menu_item_name=item.menu_item.name if item.menu_item else "Unknown",
            quantity=item.quantity,
            price=float(item.price)
        )
        for item in order.items
    ]

    return OrderResponse(
        id=order.id,
        customer_id=order.customer_id,
        restaurant_id=order.restaurant_id,
        restaurant_name=order.restaurant.name,
        status=order.status,
        total_amount=float(order.total_amount),
        created_at=order.created_at,
        items=items_response
    )


@router.post("/complete/{order_id}", response_model=OrderResponse)
async def complete_order(
    order_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(require_permission("update_order"))
):
    order = await service.complete_order(db, order_id, current_user)

    items_response: List[OrderItemResponse] = [
        OrderItemResponse(
            menu_item_id=item.menu_item_id,
            menu_item_name=item.menu_item.name if item.menu_item else "Unknown",
            quantity=item.quantity,
            price=float(item.price)
        )
        for item in order.items
    ]

    return OrderResponse(
        id=order.id,
        customer_id=order.customer_id,
        restaurant_id=order.restaurant_id,
        restaurant_name=order.restaurant.name,
        status=order.status,
        total_amount=float(order.total_amount),
        created_at=order.created_at,
        items=items_response
    )