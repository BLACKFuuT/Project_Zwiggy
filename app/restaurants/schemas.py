# app/restaurants/schemas.py

from datetime import datetime
from typing import Optional
from pydantic import BaseModel, ConfigDict
from uuid import UUID


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
    owner_id: UUID
    is_active: bool
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)


class RestaurantListResponse(BaseModel):
    id: int
    name: str
    description: Optional[str] = None
    address: str

    model_config = ConfigDict(from_attributes=True)