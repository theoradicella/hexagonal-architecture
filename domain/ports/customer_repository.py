from typing import Protocol

from domain.entities.customer import Customer


class ICustomerRepository(Protocol):
    async def save(self, customer: Customer) -> Customer: ...

    async def find_by_id(self, customer_id: int) -> Customer | None: ...

    async def find_all(self, page: int, page_size: int) -> list[Customer]: ...
