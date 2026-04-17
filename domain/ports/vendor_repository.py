from typing import Protocol

from domain.entities.vendor import Vendor


class IVendorRepository(Protocol):
    async def save(self, vendor: Vendor) -> Vendor: ...

    async def find_by_id(self, vendor_id: int) -> Vendor | None: ...

    async def find_all(self, page: int, page_size: int) -> list[Vendor]: ...
