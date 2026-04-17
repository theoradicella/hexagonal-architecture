from datetime import datetime, timezone

import pytest

from domain.entities.user import User
from domain.exceptions import InvalidCredentialsError
from domain.use_cases.auth.login import LoginUseCase
from tests.unit.stubs.fake_password_hasher import FakePasswordHasher
from tests.unit.stubs.fake_token_service import FakeTokenService
from tests.unit.stubs.in_memory_user_repository import InMemoryUserRepository


async def _seeded_repo(email: str, plaintext_password: str) -> InMemoryUserRepository:
    repo = InMemoryUserRepository()
    hasher = FakePasswordHasher()
    user = User(
        id=None,
        email=email,
        hashed_password=hasher.hash(plaintext_password),
        created_at=datetime.now(timezone.utc),
    )
    await repo.save(user)
    return repo


async def test_login_returns_token_for_valid_credentials():
    repo = await _seeded_repo("a@b.com", "pass")
    use_case = LoginUseCase(repo, FakeTokenService(), FakePasswordHasher())

    token = await use_case.execute("a@b.com", "pass")

    assert token == "token::1"


async def test_login_raises_for_unknown_email():
    repo = InMemoryUserRepository()
    use_case = LoginUseCase(repo, FakeTokenService(), FakePasswordHasher())

    with pytest.raises(InvalidCredentialsError):
        await use_case.execute("ghost@b.com", "pass")


async def test_login_raises_for_wrong_password():
    repo = await _seeded_repo("a@b.com", "correct")
    use_case = LoginUseCase(repo, FakeTokenService(), FakePasswordHasher())

    with pytest.raises(InvalidCredentialsError):
        await use_case.execute("a@b.com", "wrong")
