from domain.entities.vendor import Vendor


class InMemoryVendorRepository:
    def __init__(self) -> None:
        self.vendors: dict[int, Vendor] = {}
        self._next_id = 1

    async def save(self, vendor: Vendor) -> Vendor:
        if vendor.id is None:
            vendor.id = self._next_id
            self._next_id += 1
        self.vendors[vendor.id] = vendor
        return vendor

    async def find_by_id(self, vendor_id: int) -> Vendor | None:
        return self.vendors.get(vendor_id)

    async def find_all(self, page: int, page_size: int) -> list[Vendor]:
        items = list(self.vendors.values())
        start = (page - 1) * page_size
        return items[start : start + page_size]
