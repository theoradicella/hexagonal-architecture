from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer

from domain.entities.user import User
from domain.exceptions import InvalidCredentialsError
from domain.ports.token_service import ITokenService
from domain.ports.user_repository import IUserRepository
from infrastructure.dependencies import get_token_service, get_user_repository

bearer_scheme = HTTPBearer()


async def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(bearer_scheme),
    token_service: ITokenService = Depends(get_token_service),
    user_repo: IUserRepository = Depends(get_user_repository),
) -> User:
    try:
        user_id = await token_service.decode_token(credentials.credentials)
    except InvalidCredentialsError as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=str(e),
            headers={"WWW-Authenticate": "Bearer"},
        )

    user = await user_repo.find_by_id(int(user_id))
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User not found",
            headers={"WWW-Authenticate": "Bearer"},
        )

    return user
