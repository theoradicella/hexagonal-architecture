from datetime import datetime, timezone

from domain.entities.vendor import Vendor
from domain.ports.vendor_repository import IVendorRepository


class CreateVendorUseCase:
    def __init__(self, vendor_repository: IVendorRepository) -> None:
        self.vendor_repository = vendor_repository

    async def execute(self, name: str, contact_email: str) -> Vendor:
        vendor = Vendor(
            id=None,
            name=name,
            contact_email=contact_email,
            created_at=datetime.now(timezone.utc),
        )
        return await self.vendor_repository.save(vendor)
