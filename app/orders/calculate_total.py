from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from app.orders.models import Order, OrderItem
from app.menu_items.models import MenuItem
from app.core.database import get_db
from sqlalchemy.orm import selectinload 

router = APIRouter(prefix="/orders", tags=["Orders"])


@router.get("/calculate-total/{order_id}")
async def calculate_total(order_id: int, db: AsyncSession = Depends(get_db)):
    """
    Calculate total amount of an existing order by order_id.
    Returns each item with its total and overall total.
    """

    # Fetch the order with items
    result = await db.execute(
        select(Order)
        .where(Order.id == order_id)
        .options(
            # Eager-load items and menu items
            selectinload(Order.items).selectinload(OrderItem.menu_item)
        )
    )
    order = result.scalars().first()

    if not order:
        raise HTTPException(status_code=404, detail="Order not found")

    total_amount = 0
    items_response = []

    for item in order.items:
        price = float(item.price)  # price stored at order creation
        quantity = item.quantity
        item_total = price * quantity
        total_amount += item_total

        items_response.append({
            "menu_item_id": item.menu_item_id,
            "menu_item_name": item.menu_item.name if item.menu_item else "Unknown",
            "quantity": quantity,
            "price": price,
            "item_total": item_total
        })

    return {
        "total_amount": total_amount,
        "items": items_response
    }