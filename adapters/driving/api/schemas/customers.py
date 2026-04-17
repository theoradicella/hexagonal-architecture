from datetime import datetime

from pydantic import BaseModel


class CreateCustomerRequest(BaseModel):
    name: str


class CustomerResponse(BaseModel):
    id: int
    name: str
    created_at: datetime


class CustomerListResponse(BaseModel):
    items: list[CustomerResponse]
    total: int
    page: int
    page_size: int
