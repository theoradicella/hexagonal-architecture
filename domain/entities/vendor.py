from dataclasses import dataclass
from datetime import datetime


@dataclass
class Vendor:
    id: int | None
    name: str
    contact_email: str
    created_at: datetime
