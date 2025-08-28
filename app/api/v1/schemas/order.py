from pydantic import BaseModel, Field
from typing import List
from datetime import datetime
from .customer import OrderCustomer, CustomerResponse
from .item import OrderItemBase, OrderItemResponse
import uuid

class OrderData(BaseModel):
    items: List[OrderItemBase]

class OrderCreate(BaseModel):
    customer: OrderCustomer
    order: OrderData

class OrderResponse(BaseModel):
    id: uuid.UUID
    order_id: str = Field(alias="order_number")

    status: str
    total_value: float
    customer: CustomerResponse
    items: List[OrderItemResponse]
    created_at: datetime

    class Config:
        from_attributes = True
        populate_by_name = True

class OrderStatusUpdate(BaseModel):
    status: str = Field(..., max_length=20)  # e.g., "PENDING", "SHIPPED", "DELIVERED"

class OrderSummaryResponse(BaseModel):
    total_orders: int
    orders_by_status: dict[str, int]
    total_revenue: float