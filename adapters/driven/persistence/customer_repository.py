from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from adapters.driven.persistence.models import CustomerModel
from domain.entities.customer import Customer


class SqlAlchemyCustomerRepository:
    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def save(self, customer: Customer) -> Customer:
        model = CustomerModel.from_entity(customer)
        self.session.add(model)
        await self.session.commit()
        await self.session.refresh(model)
        return model.to_entity()

    async def find_by_id(self, customer_id: int) -> Customer | None:
        result = await self.session.execute(
            select(CustomerModel).where(CustomerModel.id == customer_id)
        )
        model = result.scalars().first()
        if model is None:
            return None
        return model.to_entity()

    async def find_all(self, page: int, page_size: int) -> list[Customer]:
        result = await self.session.execute(
            select(CustomerModel).offset((page - 1) * page_size).limit(page_size)
        )
        return [model.to_entity() for model in result.scalars().all()]
