from domain.exceptions import InvalidCredentialsError
from domain.ports.password_hasher import IPasswordHasher
from domain.ports.token_service import ITokenService
from domain.ports.user_repository import IUserRepository


class LoginUseCase:
    def __init__(
        self,
        user_repository: IUserRepository,
        token_service: ITokenService,
        password_hasher: IPasswordHasher,
    ) -> None:
        self.user_repository = user_repository
        self.token_service = token_service
        self.password_hasher = password_hasher

    async def execute(self, email: str, password: str) -> str:
        user = await self.user_repository.find_by_email(email)
        if user is None:
            raise InvalidCredentialsError("Invalid email or password")

        if not self.password_hasher.verify(password, user.hashed_password):
            raise InvalidCredentialsError("Invalid email or password")

        assert user.id is not None
        return await self.token_service.create_access_token(user.id)
