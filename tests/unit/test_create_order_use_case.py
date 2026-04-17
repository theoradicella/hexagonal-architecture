from datetime import datetime, timezone

import pytest

from domain.entities.customer import Customer
from domain.entities.order import OrderStatus
from domain.entities.vendor import Vendor
from domain.exceptions import CustomerNotFoundError, VendorNotFoundError
from domain.use_cases.orders.create_order import CreateOrderUseCase
from tests.unit.stubs.in_memory_customer_repository import InMemoryCustomerRepository
from tests.unit.stubs.in_memory_order_repository import InMemoryOrderRepository
from tests.unit.stubs.in_memory_vendor_repository import InMemoryVendorRepository


async def _seed_customer_and_vendor() -> tuple[InMemoryCustomerRepository, InMemoryVendorRepository]:
    customer_repo = InMemoryCustomerRepository()
    vendor_repo = InMemoryVendorRepository()
    await customer_repo.save(
        Customer(id=None, name="Acme", created_at=datetime.now(timezone.utc))
    )
    await vendor_repo.save(
        Vendor(
            id=None,
            name="Widgets Inc",
            contact_email="v@w.com",
            created_at=datetime.now(timezone.utc),
        )
    )
    return customer_repo, vendor_repo


async def test_create_order_saves_with_correct_data():
    customer_repo, vendor_repo = await _seed_customer_and_vendor()
    order_repo = InMemoryOrderRepository()
    use_case = CreateOrderUseCase(order_repo, customer_repo, vendor_repo)

    order = await use_case.execute(customer_id=1, vendor_id=1, total_amount=100)

    assert order.id == 1
    assert order.customer_id == 1
    assert order.vendor_id == 1
    assert order.total_amount == 100
    assert order.status == OrderStatus.PENDING
    assert len(order_repo.orders) == 1


async def test_create_order_raises_when_customer_missing():
    _, vendor_repo = await _seed_customer_and_vendor()
    order_repo = InMemoryOrderRepository()
    empty_customers = InMemoryCustomerRepository()
    use_case = CreateOrderUseCase(order_repo, empty_customers, vendor_repo)

    with pytest.raises(CustomerNotFoundError):
        await use_case.execute(customer_id=999, vendor_id=1, total_amount=100)

    assert len(order_repo.orders) == 0


async def test_create_order_raises_when_vendor_missing():
    customer_repo, _ = await _seed_customer_and_vendor()
    order_repo = InMemoryOrderRepository()
    empty_vendors = InMemoryVendorRepository()
    use_case = CreateOrderUseCase(order_repo, customer_repo, empty_vendors)

    with pytest.raises(VendorNotFoundError):
        await use_case.execute(customer_id=1, vendor_id=999, total_amount=100)

    assert len(order_repo.orders) == 0
