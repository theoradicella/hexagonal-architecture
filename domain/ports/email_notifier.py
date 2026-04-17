from typing import Protocol

from domain.entities.order import Order
from domain.entities.vendor import Vendor


class IEmailNotifier(Protocol):
    async def send_order_confirmation(self, order: Order, vendor: Vendor) -> None: ...

    async def send_status_update(self, order: Order, vendor: Vendor) -> None: ...
