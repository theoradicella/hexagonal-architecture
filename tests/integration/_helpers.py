from httpx import AsyncClient


async def register_and_login(
    client: AsyncClient, email: str = "alice@example.com", password: str = "secret"
) -> dict[str, str]:
    await client.post(
        "/api/v1/auth/register",
        json={"email": email, "password": password},
    )
    response = await client.post(
        "/api/v1/auth/login",
        json={"email": email, "password": password},
    )
    token = response.json()["access_token"]
    return {"Authorization": f"Bearer {token}"}
