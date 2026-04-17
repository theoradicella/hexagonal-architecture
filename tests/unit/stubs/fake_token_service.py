class FakeTokenService:
    async def create_access_token(self, user_id: int) -> str:
        return f"token::{user_id}"

    async def decode_token(self, token: str) -> str:
        return token.removeprefix("token::")
