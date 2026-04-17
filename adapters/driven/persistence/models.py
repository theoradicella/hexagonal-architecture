from datetime import datetime

from sqlalchemy import DateTime, ForeignKey, Integer, String
from sqlalchemy.orm import Mapped, mapped_column

from domain.entities.customer import Customer
from domain.entities.order import Order, OrderStatus
from domain.entities.user import User
from domain.entities.vendor import Vendor
from infrastructure.database import Base


class UserModel(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    email: Mapped[str] = mapped_column(String(255), unique=True, nullable=False)
    hashed_password: Mapped[str] = mapped_column(String(255), nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime, nullable=False)

    @classmethod
    def from_entity(cls, user: User) -> "UserModel":
        return cls(
            id=user.id,
            email=user.email,
            hashed_password=user.hashed_password,
            created_at=user.created_at,
        )

    def to_entity(self) -> User:
        return User(
            id=self.id,
            email=self.email,
            hashed_password=self.hashed_password,
            created_at=self.created_at,
        )


class CustomerModel(Base):
    __tablename__ = "customers"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime, nullable=False)

    @classmethod
    def from_entity(cls, customer: Customer) -> "CustomerModel":
        return cls(
            id=customer.id,
            name=customer.name,
            created_at=customer.created_at,
        )

    def to_entity(self) -> Customer:
        return Customer(
            id=self.id,
            name=self.name,
            created_at=self.created_at,
        )


class VendorModel(Base):
    __tablename__ = "vendors"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    contact_email: Mapped[str] = mapped_column(String(255), unique=True, nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime, nullable=False)

    @classmethod
    def from_entity(cls, vendor: Vendor) -> "VendorModel":
        return cls(
            id=vendor.id,
            name=vendor.name,
            contact_email=vendor.contact_email,
            created_at=vendor.created_at,
        )

    def to_entity(self) -> Vendor:
        return Vendor(
            id=self.id,
            name=self.name,
            contact_email=self.contact_email,
            created_at=self.created_at,
        )


class OrderModel(Base):
    __tablename__ = "orders"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    customer_id: Mapped[int] = mapped_column(Integer, ForeignKey("customers.id"), nullable=False)
    vendor_id: Mapped[int] = mapped_column(Integer, ForeignKey("vendors.id"), nullable=False)
    status: Mapped[str] = mapped_column(String(20), nullable=False)
    total_amount: Mapped[int] = mapped_column(Integer, nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime, nullable=False)

    @classmethod
    def from_entity(cls, order: Order) -> "OrderModel":
        return cls(
            id=order.id,
            customer_id=order.customer_id,
            vendor_id=order.vendor_id,
            status=order.status.value,
            total_amount=order.total_amount,
            created_at=order.created_at,
        )

    def to_entity(self) -> Order:
        return Order(
            id=self.id,
            customer_id=self.customer_id,
            vendor_id=self.vendor_id,
            status=OrderStatus(self.status),
            total_amount=self.total_amount,
            created_at=self.created_at,
        )
