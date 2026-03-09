from datetime import datetime
from typing import List, Optional
from pydantic import BaseModel
from uuid import UUID


class OrderItemCreate(BaseModel):
    menu_item_id: int
    quantity: int


class OrderCreate(BaseModel):
    restaurant_id: int
    items: List[OrderItemCreate]        


class OrderItemResponse(BaseModel):
    menu_item_id: int
    menu_item_name: str
    quantity: int
    price: float


class OrderResponse(BaseModel):
    id: int
    customer_id: UUID
    restaurant_id: int
    restaurant_name: str
    status: str
    total_amount: float
    created_at: datetime
    items: List[OrderItemResponse]
    
    