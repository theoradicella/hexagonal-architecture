import pytest

from domain.exceptions import UserAlreadyExistsError
from domain.use_cases.auth.register import RegisterUseCase
from tests.unit.stubs.fake_password_hasher import FakePasswordHasher
from tests.unit.stubs.in_memory_user_repository import InMemoryUserRepository


async def test_register_creates_user_with_hashed_password():
    repo = InMemoryUserRepository()
    hasher = FakePasswordHasher()
    use_case = RegisterUseCase(repo, hasher)

    user = await use_case.execute("a@b.com", "plaintext")

    assert user.id == 1
    assert user.email == "a@b.com"
    assert user.hashed_password == "hashed::plaintext"
    assert user.hashed_password != "plaintext"


async def test_register_persists_user_in_repository():
    repo = InMemoryUserRepository()
    use_case = RegisterUseCase(repo, FakePasswordHasher())

    await use_case.execute("a@b.com", "pass")

    assert len(repo.users) == 1
    assert repo.users[1].email == "a@b.com"


async def test_register_rejects_duplicate_email():
    repo = InMemoryUserRepository()
    use_case = RegisterUseCase(repo, FakePasswordHasher())
    await use_case.execute("a@b.com", "pass")

    with pytest.raises(UserAlreadyExistsError):
        await use_case.execute("a@b.com", "different-pass")

    assert len(repo.users) == 1
