# app/restaurants/schemas.py

from datetime import datetime
from typing import Optional
from pydantic import BaseModel


class RestaurantBase(BaseModel):
    name: str
    description: Optional[str] = None
    address: str


class RestaurantCreate(RestaurantBase):
    pass


class RestaurantUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    address: Optional[str] = None
    is_active: Optional[bool] = None


class RestaurantResponse(RestaurantBase):
    id: int
    # owner_id: int
    is_active: bool
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True