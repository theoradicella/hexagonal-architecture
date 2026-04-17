from datetime import datetime, timezone

import pytest

from domain.entities.order import Order, OrderStatus
from domain.exceptions import InvalidStatusTransitionError, OrderNotFoundError
from domain.use_cases.orders.transition_order_status import TransitionOrderStatusUseCase
from tests.unit.stubs.in_memory_order_repository import InMemoryOrderRepository


async def _seed_order(status: OrderStatus = OrderStatus.PENDING) -> InMemoryOrderRepository:
    repo = InMemoryOrderRepository()
    await repo.save(
        Order(
            id=None,
            customer_id=1,
            vendor_id=1,
            status=status,
            total_amount=100,
            created_at=datetime.now(timezone.utc),
        )
    )
    return repo


async def test_valid_transition_updates_status():
    repo = await _seed_order(OrderStatus.PENDING)
    use_case = TransitionOrderStatusUseCase(repo)

    order = await use_case.execute(order_id=1, new_status=OrderStatus.CONFIRMED)

    assert order.status == OrderStatus.CONFIRMED
    assert repo.orders[1].status == OrderStatus.CONFIRMED


async def test_invalid_transition_raises():
    repo = await _seed_order(OrderStatus.DELIVERED)
    use_case = TransitionOrderStatusUseCase(repo)

    with pytest.raises(InvalidStatusTransitionError):
        await use_case.execute(order_id=1, new_status=OrderStatus.PENDING)

    assert repo.orders[1].status == OrderStatus.DELIVERED


async def test_missing_order_raises():
    repo = InMemoryOrderRepository()
    use_case = TransitionOrderStatusUseCase(repo)

    with pytest.raises(OrderNotFoundError):
        await use_case.execute(order_id=999, new_status=OrderStatus.CONFIRMED)
