from httpx import AsyncClient

from tests.integration._helpers import register_and_login


async def test_create_and_list_customers(async_client: AsyncClient):
    headers = await register_and_login(async_client)

    create_response = await async_client.post(
        "/api/v1/customers",
        headers=headers,
        json={"name": "Acme Corp"},
    )
    assert create_response.status_code == 201
    customer = create_response.json()
    assert customer["id"] == 1
    assert customer["name"] == "Acme Corp"

    list_response = await async_client.get("/api/v1/customers", headers=headers)
    assert list_response.status_code == 200
    data = list_response.json()
    assert data["total"] == 1
    assert data["items"][0]["name"] == "Acme Corp"


async def test_list_customers_respects_pagination(async_client: AsyncClient):
    headers = await register_and_login(async_client)

    for i in range(5):
        await async_client.post(
            "/api/v1/customers",
            headers=headers,
            json={"name": f"Customer {i}"},
        )

    response = await async_client.get(
        "/api/v1/customers?page=1&page_size=2",
        headers=headers,
    )
    assert response.status_code == 200
    assert len(response.json()["items"]) == 2
