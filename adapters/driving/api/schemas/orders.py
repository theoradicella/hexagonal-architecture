from datetime import datetime

from pydantic import BaseModel

from domain.entities.order import OrderStatus


class CreateOrderRequest(BaseModel):
    customer_id: int
    vendor_id: int
    total_amount: int


class OrderResponse(BaseModel):
    id: int
    customer_id: int
    vendor_id: int
    status: OrderStatus
    total_amount: int
    created_at: datetime


class OrderListResponse(BaseModel):
    items: list[OrderResponse]
    total: int
    page: int
    page_size: int


class TransitionStatusRequest(BaseModel):
    status: OrderStatus
