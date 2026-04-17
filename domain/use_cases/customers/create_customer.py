from datetime import datetime, timezone

from domain.entities.customer import Customer
from domain.ports.customer_repository import ICustomerRepository


class CreateCustomerUseCase:
    def __init__(self, customer_repository: ICustomerRepository) -> None:
        self.customer_repository = customer_repository

    async def execute(self, name: str) -> Customer:
        customer = Customer(id=None, name=name, created_at=datetime.now(timezone.utc))
        return await self.customer_repository.save(customer)
