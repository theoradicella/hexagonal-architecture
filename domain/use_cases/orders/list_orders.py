from domain.entities.order import Order, OrderStatus
from domain.ports.order_repository import IOrderRepository


class ListOrdersUseCase:
    def __init__(self, order_repository: IOrderRepository) -> None:
        self.order_repository = order_repository

    async def execute(
        self,
        page: int,
        page_size: int,
        status: OrderStatus | None = None,
        customer_id: int | None = None,
        vendor_id: int | None = None,
    ) -> list[Order]:
        return await self.order_repository.find_all(
            page=page,
            page_size=page_size,
            status=status,
            customer_id=customer_id,
            vendor_id=vendor_id,
        )
