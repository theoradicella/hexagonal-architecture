from domain.entities.order import Order, OrderStatus


class InMemoryOrderRepository:
    def __init__(self) -> None:
        self.orders: dict[int, Order] = {}
        self._next_id = 1

    async def save(self, order: Order) -> Order:
        if order.id is None:
            order.id = self._next_id
            self._next_id += 1
        self.orders[order.id] = order
        return order

    async def find_by_id(self, order_id: int) -> Order | None:
        return self.orders.get(order_id)

    async def find_all(
        self,
        page: int,
        page_size: int,
        status: OrderStatus | None = None,
        customer_id: int | None = None,
        vendor_id: int | None = None,
    ) -> list[Order]:
        items = list(self.orders.values())
        if status is not None:
            items = [o for o in items if o.status == status]
        if customer_id is not None:
            items = [o for o in items if o.customer_id == customer_id]
        if vendor_id is not None:
            items = [o for o in items if o.vendor_id == vendor_id]
        start = (page - 1) * page_size
        return items[start : start + page_size]
