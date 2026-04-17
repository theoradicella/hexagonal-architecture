from httpx import AsyncClient


async def test_register_creates_user(async_client: AsyncClient):
    response = await async_client.post(
        "/api/v1/auth/register",
        json={"email": "alice@example.com", "password": "secret"},
    )

    assert response.status_code == 201
    data = response.json()
    assert data["email"] == "alice@example.com"
    assert "hashed_password" not in data
    assert data["id"] == 1


async def test_register_rejects_duplicate_email(async_client: AsyncClient):
    await async_client.post(
        "/api/v1/auth/register",
        json={"email": "alice@example.com", "password": "secret"},
    )
    response = await async_client.post(
        "/api/v1/auth/register",
        json={"email": "alice@example.com", "password": "different"},
    )

    assert response.status_code == 409


async def test_login_returns_token(async_client: AsyncClient):
    await async_client.post(
        "/api/v1/auth/register",
        json={"email": "alice@example.com", "password": "secret"},
    )

    response = await async_client.post(
        "/api/v1/auth/login",
        json={"email": "alice@example.com", "password": "secret"},
    )

    assert response.status_code == 200
    data = response.json()
    assert "access_token" in data
    assert data["token_type"] == "bearer"


async def test_login_rejects_wrong_password(async_client: AsyncClient):
    await async_client.post(
        "/api/v1/auth/register",
        json={"email": "alice@example.com", "password": "secret"},
    )

    response = await async_client.post(
        "/api/v1/auth/login",
        json={"email": "alice@example.com", "password": "wrong"},
    )

    assert response.status_code == 401


async def test_protected_route_requires_token(async_client: AsyncClient):
    response = await async_client.get("/api/v1/customers")
    assert response.status_code in (401, 403)
