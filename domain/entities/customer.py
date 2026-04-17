from dataclasses import dataclass
from datetime import datetime


@dataclass
class Customer:
    id: int | None
    name: str
    created_at: datetime
