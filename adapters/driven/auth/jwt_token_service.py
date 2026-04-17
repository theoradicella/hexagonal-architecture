from datetime import datetime, timedelta, timezone

from jose import JWTError, jwt

from domain.exceptions import InvalidCredentialsError


class JwtTokenService:
    def __init__(self, secret_key: str, algorithm: str, expire_minutes: int) -> None:
        self.secret_key = secret_key
        self.algorithm = algorithm
        self.expire_minutes = expire_minutes

    async def create_access_token(self, user_id: int) -> str:
        expire = datetime.now(timezone.utc) + timedelta(minutes=self.expire_minutes)
        payload = {"sub": str(user_id), "exp": expire}
        return jwt.encode(payload, self.secret_key, algorithm=self.algorithm)

    async def decode_token(self, token: str) -> str:
        try:
            payload = jwt.decode(token, self.secret_key, algorithms=[self.algorithm])
            user_id: str | None = payload.get("sub")
            if user_id is None:
                raise InvalidCredentialsError("Invalid token: no user ID")
            return user_id
        except JWTError:
            raise InvalidCredentialsError("Invalid or expired token")
