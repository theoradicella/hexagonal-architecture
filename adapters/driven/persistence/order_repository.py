from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from adapters.driven.persistence.models import OrderModel
from domain.entities.order import Order, OrderStatus


class SqlAlchemyOrderRepository:
    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def save(self, order: Order) -> Order:
        model = OrderModel.from_entity(order)
        merged = await self.session.merge(model)
        await self.session.commit()
        await self.session.refresh(merged)
        return merged.to_entity()

    async def find_by_id(self, order_id: int) -> Order | None:
        result = await self.session.execute(
            select(OrderModel).where(OrderModel.id == order_id)
        )
        model = result.scalars().first()
        if model is None:
            return None
        return model.to_entity()

    async def find_all(
        self,
        page: int,
        page_size: int,
        status: OrderStatus | None = None,
        customer_id: int | None = None,
        vendor_id: int | None = None,
    ) -> list[Order]:
        query = select(OrderModel)

        if status is not None:
            query = query.where(OrderModel.status == status.value)
        if customer_id is not None:
            query = query.where(OrderModel.customer_id == customer_id)
        if vendor_id is not None:
            query = query.where(OrderModel.vendor_id == vendor_id)

        query = query.offset((page - 1) * page_size).limit(page_size)

        result = await self.session.execute(query)
        return [model.to_entity() for model in result.scalars().all()]
