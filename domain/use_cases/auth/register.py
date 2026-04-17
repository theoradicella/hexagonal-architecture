from datetime import datetime, timezone

from domain.entities.user import User
from domain.exceptions import UserAlreadyExistsError
from domain.ports.password_hasher import IPasswordHasher
from domain.ports.user_repository import IUserRepository


class RegisterUseCase:
    def __init__(
        self, user_repository: IUserRepository, password_hasher: IPasswordHasher
    ) -> None:
        self.user_repository = user_repository
        self.password_hasher = password_hasher

    async def execute(self, email: str, password: str) -> User:
        existing = await self.user_repository.find_by_email(email)
        if existing is not None:
            raise UserAlreadyExistsError(f"User with email {email} already exists")

        hashed_password = self.password_hasher.hash(password)

        user = User(
            id=None,
            email=email,
            hashed_password=hashed_password,
            created_at=datetime.now(timezone.utc),
        )

        return await self.user_repository.save(user)
