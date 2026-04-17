from datetime import datetime, timezone

from domain.entities.order import Order, OrderStatus
from domain.exceptions import CustomerNotFoundError, VendorNotFoundError
from domain.ports.customer_repository import ICustomerRepository
from domain.ports.order_repository import IOrderRepository
from domain.ports.vendor_repository import IVendorRepository


class CreateOrderUseCase:
    def __init__(
        self,
        order_repository: IOrderRepository,
        customer_repository: ICustomerRepository,
        vendor_repository: IVendorRepository,
    ) -> None:
        self.order_repository = order_repository
        self.customer_repository = customer_repository
        self.vendor_repository = vendor_repository

    async def execute(self, customer_id: int, vendor_id: int, total_amount: int) -> Order:
        customer = await self.customer_repository.find_by_id(customer_id)
        if customer is None:
            raise CustomerNotFoundError(f"Customer {customer_id} not found")

        vendor = await self.vendor_repository.find_by_id(vendor_id)
        if vendor is None:
            raise VendorNotFoundError(f"Vendor {vendor_id} not found")

        order = Order(
            id=None,
            customer_id=customer_id,
            vendor_id=vendor_id,
            status=OrderStatus.PENDING,
            total_amount=total_amount,
            created_at=datetime.now(timezone.utc),
        )
        return await self.order_repository.save(order)
