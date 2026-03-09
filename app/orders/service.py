from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.orm import selectinload
from fastapi import HTTPException

from app.orders.repository import OrderRepository
from app.orders.models import Order, OrderItem
from app.orders.schemas import OrderCreate
from app.users.models import User
from app.restaurants.repository import RestaurantRepository
from app.menu_items.repository import MenuItemRepository
from app.events.tasks import publish_order_event_task
from app.events.tasks import send_order_email


class OrderService:
    def __init__(self):
        self.repository = OrderRepository()
        self.restaurant_repo = RestaurantRepository()
        self.menu_repo = MenuItemRepository()

    # -------------------------------
    # Create a new order
    # -------------------------------
    async def create_order(self, db: AsyncSession, data: OrderCreate, current_user: User):

        restaurant = await self.restaurant_repo.get_by_id(db, data.restaurant_id)
        if not restaurant:
            raise HTTPException(status_code=404, detail="Restaurant not found")
                                                                                            
        order = Order(
            customer_id=current_user.id,
            restaurant_id=data.restaurant_id,
            status="PENDING"
        )

        await self.repository.create_order(db, order)

        total_amount = 0
        order_items_list = []

        for item in data.items:

            menu_item = await self.menu_repo.get_by_id(db, item.menu_item_id)

            if not menu_item:
                raise HTTPException(
                    status_code=404,
                    detail=f"Menu item {item.menu_item_id} not found"
                )

            order_item = OrderItem(
                order_id=order.id,
                menu_item_id=item.menu_item_id,
                quantity=item.quantity,
                price=menu_item.price
            )

            await self.repository.create_order_item(db, order_item)

            total_amount += float(menu_item.price) * item.quantity

            order_items_list.append(order_item)

        await self.repository.update_order_total(db, order.id, total_amount)

        await db.commit()
        
        send_order_email.delay(
        current_user.email,
        order.id,
        total_amount
)
        

        # reload order with relations
        result = await db.execute(
            select(Order)
            .options(
                selectinload(Order.items).selectinload(OrderItem.menu_item),
                selectinload(Order.restaurant)
            )
            .where(Order.id == order.id)
        )

        order = result.scalars().first()

        # -----------------------------
        # Create payload for Celery
        # -----------------------------
        order_payload = {
            "event_type": "ORDER_CREATED",
            "order_id": order.id,
            "customer_id": str(order.customer_id),
            "restaurant_id": order.restaurant_id,
            "status": order.status,
            "total_amount": float(order.total_amount),
            "items": [
                {
                    "menu_item_id": item.menu_item_id,
                    "quantity": item.quantity,
                    "price": float(item.price)
                }
                for item in order_items_list
            ]
        }

        # Send event to Celery
        publish_order_event_task.delay(order_payload)

        return order

    # -------------------------------
    # Get order
    # -------------------------------
    async def get_order(self, db: AsyncSession, order_id: int, current_user: User):

        result = await db.execute(
            select(Order)
            .options(
                selectinload(Order.items).selectinload(OrderItem.menu_item),
                selectinload(Order.restaurant)
            )
            .where(Order.id == order_id)
        )

        order = result.scalars().first()

        if not order:
            raise HTTPException(status_code=404, detail="Order not found")

        if order.customer_id != current_user.id and order.restaurant.owner_id != current_user.id:
            raise HTTPException(status_code=403, detail="Not authorized to view this order")

        return order

    # -------------------------------
    # Complete order
    # -------------------------------
    async def complete_order(self, db: AsyncSession, order_id: int, current_user: User):

        result = await db.execute(
            select(Order)
            .options(
                selectinload(Order.restaurant),
                selectinload(Order.items).selectinload(OrderItem.menu_item)
            )
            .where(Order.id == order_id)
        )

        order = result.scalars().first()

        if not order:
            raise HTTPException(status_code=404, detail="Order not found")

        if order.restaurant.owner_id != current_user.id:
            raise HTTPException(
                status_code=403,
                detail="Not authorized to complete this order"
            )

        order.status = "COMPLETED"

        await self.repository.update_status(db, order.id, "COMPLETED")

        await db.commit()

        # -----------------------------
        # Create payload for Celery
        # -----------------------------
        order_payload = {
            "event_type": "ORDER_COMPLETED",
            "order_id": order.id,
            "customer_id": str(order.customer_id),
            "restaurant_id": order.restaurant_id,
            "status": order.status,
            "total_amount": float(order.total_amount),
            "items": [
                {
                    "menu_item_id": item.menu_item_id,
                    "quantity": item.quantity,
                    "price": float(item.price)
                }
                for item in order.items
            ]
        }

        # Send event to Celery
        publish_order_event_task.delay(order_payload)

        return order