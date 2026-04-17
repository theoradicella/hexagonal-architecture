from datetime import datetime

from pydantic import BaseModel, EmailStr


class CreateVendorRequest(BaseModel):
    name: str
    contact_email: EmailStr


class VendorResponse(BaseModel):
    id: int
    name: str
    contact_email: EmailStr
    created_at: datetime


class VendorListResponse(BaseModel):
    items: list[VendorResponse]
    total: int
    page: int
    page_size: int
