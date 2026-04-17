from dataclasses import dataclass, field

from domain.entities.order import Order
from domain.entities.vendor import Vendor


@dataclass
class SentEmail:
    to: str
    subject: str
    body: str


@dataclass
class InMemoryEmailNotifier:
    emails: list[SentEmail] = field(default_factory=list)

    async def send_order_confirmation(self, order: Order, vendor: Vendor) -> None:
        self.emails.append(
            SentEmail(
                to=vendor.contact_email,
                subject=f"Order #{order.id} confirmed",
                body=f"New order #{order.id} received. Total: {order.total_amount}.",
            )
        )

    async def send_status_update(self, order: Order, vendor: Vendor) -> None:
        self.emails.append(
            SentEmail(
                to=vendor.contact_email,
                subject=f"Order #{order.id} status update",
                body=f"Order #{order.id} is now {order.status.value}.",
            )
        )
