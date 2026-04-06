from datetime import datetime

from pydantic import BaseModel


class Order(BaseModel):
    order_id: str
    customer_id: str
    amount: float
    status: str
    created_at: datetime


class Customer(BaseModel):
    customer_id: str
    first_name: str
    email: str
    created_at: datetime
    updated_at: datetime
    is_deleted: bool = False
