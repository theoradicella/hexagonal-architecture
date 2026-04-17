from domain.entities.customer import Customer
from domain.ports.customer_repository import ICustomerRepository


class ListCustomersUseCase:
    def __init__(self, customer_repository: ICustomerRepository) -> None:
        self.customer_repository = customer_repository

    async def execute(self, page: int, page_size: int) -> list[Customer]:
        customers = await self.customer_repository.find_all(
            page=page, page_size=page_size
        )
        return customers
