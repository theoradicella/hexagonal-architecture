from typing import Protocol

from domain.entities.order import Order, OrderStatus


class IOrderRepository(Protocol):
    async def save(self, order: Order) -> Order: ...

    async def find_by_id(self, order_id: int) -> Order | None: ...

    async def find_all(
        self,
        page: int,
        page_size: int,
        status: OrderStatus | None = None,
        customer_id: int | None = None,
        vendor_id: int | None = None,
    ) -> list[Order]: ...
