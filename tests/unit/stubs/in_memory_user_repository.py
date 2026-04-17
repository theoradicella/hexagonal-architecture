from domain.entities.user import User


class InMemoryUserRepository:
    def __init__(self) -> None:
        self.users: dict[int, User] = {}
        self._next_id = 1

    async def save(self, user: User) -> User:
        if user.id is None:
            user.id = self._next_id
            self._next_id += 1
        self.users[user.id] = user
        return user

    async def find_by_email(self, email: str) -> User | None:
        return next((u for u in self.users.values() if u.email == email), None)

    async def find_by_id(self, user_id: int) -> User | None:
        return self.users.get(user_id)
