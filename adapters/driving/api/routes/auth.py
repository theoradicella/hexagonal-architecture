from fastapi import APIRouter, Depends, HTTPException, status

from adapters.driving.api.schemas.auth import (
    LoginRequest,
    RegisterRequest,
    TokenResponse,
    UserResponse,
)
from domain.exceptions import InvalidCredentialsError, UserAlreadyExistsError
from domain.use_cases.auth.login import LoginUseCase
from domain.use_cases.auth.register import RegisterUseCase
from infrastructure.dependencies import get_login_use_case, get_register_use_case

router = APIRouter(prefix="/auth", tags=["auth"])


@router.post(
    "/register",
    response_model=UserResponse,
    status_code=status.HTTP_201_CREATED,
)
async def register(
    payload: RegisterRequest,
    use_case: RegisterUseCase = Depends(get_register_use_case),
) -> UserResponse:
    try:
        user = await use_case.execute(payload.email, payload.password)
    except UserAlreadyExistsError as e:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=str(e),
        )

    assert user.id is not None
    return UserResponse(
        id=user.id,
        email=user.email,
        created_at=user.created_at,
    )


@router.post(
    "/login",
    response_model=TokenResponse,
    status_code=status.HTTP_200_OK,
)
async def login(
    payload: LoginRequest, use_case: LoginUseCase = Depends(get_login_use_case)
) -> TokenResponse:
    try:
        access_token = await use_case.execute(payload.email, payload.password)
    except InvalidCredentialsError as e:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=str(e))

    return TokenResponse(access_token=access_token)
