from typing import Protocol

from domain.entities.user import User


class IUserRepository(Protocol):
    async def save(self, user: User) -> User: ...

    async def find_by_email(self, email: str) -> User | None: ...

    async def find_by_id(self, user_id: int) -> User | None: ...
