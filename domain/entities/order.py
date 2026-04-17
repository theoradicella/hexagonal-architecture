import enum
from dataclasses import dataclass
from datetime import datetime

from domain.exceptions import InvalidStatusTransitionError


class OrderStatus(enum.Enum):
    PENDING = "PENDING"
    CONFIRMED = "CONFIRMED"
    SHIPPED = "SHIPPED"
    DELIVERED = "DELIVERED"
    CANCELLED = "CANCELLED"


_ALLOWED_TRANSITIONS: dict[OrderStatus, set[OrderStatus]] = {
    OrderStatus.PENDING: {OrderStatus.CONFIRMED, OrderStatus.CANCELLED},
    OrderStatus.CONFIRMED: {OrderStatus.SHIPPED, OrderStatus.CANCELLED},
    OrderStatus.SHIPPED: {OrderStatus.DELIVERED},
}


@dataclass
class Order:
    id: int | None
    customer_id: int
    vendor_id: int
    status: OrderStatus
    total_amount: int
    created_at: datetime

    def transition_to(self, new_status: OrderStatus) -> None:
        allowed = _ALLOWED_TRANSITIONS.get(self.status, set())
        if new_status not in allowed:
            raise InvalidStatusTransitionError(
                f"Cannot transition from {self.status.value} to {new_status.value}"
            )
        self.status = new_status
