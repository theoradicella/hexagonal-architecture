from domain.entities.customer import Customer


class InMemoryCustomerRepository:
    def __init__(self) -> None:
        self.customers: dict[int, Customer] = {}
        self._next_id = 1

    async def save(self, customer: Customer) -> Customer:
        if customer.id is None:
            customer.id = self._next_id
            self._next_id += 1
        self.customers[customer.id] = customer
        return customer

    async def find_by_id(self, customer_id: int) -> Customer | None:
        return self.customers.get(customer_id)

    async def find_all(self, page: int, page_size: int) -> list[Customer]:
        items = list(self.customers.values())
        start = (page - 1) * page_size
        return items[start : start + page_size]
