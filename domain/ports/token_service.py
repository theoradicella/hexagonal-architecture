from typing import Protocol


class ITokenService(Protocol):
    async def create_access_token(self, user_id: int) -> str: ...

    async def decode_token(self, token: str) -> str: ...
