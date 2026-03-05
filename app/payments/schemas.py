from datetime import datetime
from pydantic import BaseModel


class PaymentCreate(BaseModel):
    order_id: int


class PaymentResponse(BaseModel):
    id: int
    order_id: int
    amount: float
    status: str
    provider: str
    transaction_id: str | None
    created_at: datetime

    class Config:
        from_attributes = True