from domain.entities.vendor import Vendor
from domain.ports.vendor_repository import IVendorRepository


class ListVendorsUseCase:
    def __init__(self, vendor_repository: IVendorRepository) -> None:
        self.vendor_repository = vendor_repository

    async def execute(self, page: int, page_size: int) -> list[Vendor]:
        return await self.vendor_repository.find_all(page=page, page_size=page_size)
