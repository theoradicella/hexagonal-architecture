from domain.entities.order import Order, OrderStatus
from domain.exceptions import OrderNotFoundError
from domain.ports.order_repository import IOrderRepository


class CancelOrderUseCase:
    def __init__(self, order_repository: IOrderRepository) -> None:
        self.order_repository = order_repository

    async def execute(self, order_id: int) -> Order:
        order = await self.order_repository.find_by_id(order_id)
        if order is None:
            raise OrderNotFoundError(f"Order {order_id} not found")

        order.transition_to(OrderStatus.CANCELLED)
        return await self.order_repository.save(order)
