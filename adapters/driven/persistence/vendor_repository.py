from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from adapters.driven.persistence.models import VendorModel
from domain.entities.vendor import Vendor


class SqlAlchemyVendorRepository:
    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def save(self, vendor: Vendor) -> Vendor:
        model = VendorModel.from_entity(vendor)
        self.session.add(model)
        await self.session.commit()
        await self.session.refresh(model)
        return model.to_entity()

    async def find_by_id(self, vendor_id: int) -> Vendor | None:
        result = await self.session.execute(
            select(VendorModel).where(VendorModel.id == vendor_id)
        )
        model = result.scalars().first()
        if model is None:
            return None
        return model.to_entity()

    async def find_all(self, page: int, page_size: int) -> list[Vendor]:
        result = await self.session.execute(
            select(VendorModel).offset((page - 1) * page_size).limit(page_size)
        )
        return [model.to_entity() for model in result.scalars().all()]
