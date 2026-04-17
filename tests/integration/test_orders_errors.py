from httpx import AsyncClient

from tests.integration._helpers import register_and_login


async def test_transition_missing_order_returns_404(async_client: AsyncClient):
    headers = await register_and_login(async_client)

    response = await async_client.patch(
        "/api/v1/orders/999/status",
        headers=headers,
        json={"status": "CONFIRMED"},
    )
    assert response.status_code == 404


async def test_invalid_transition_returns_422(async_client: AsyncClient):
    headers = await register_and_login(async_client)
    customer = await async_client.post(
        "/api/v1/customers",
        headers=headers,
        json={"name": "Acme Corp"},
    )
    vendor = await async_client.post(
        "/api/v1/vendors",
        headers=headers,
        json={"name": "Widgets Inc", "contact_email": "v@w.com"},
    )

    order = await async_client.post(
        "/api/v1/orders",
        headers=headers,
        json={
            "customer_id": customer.json()["id"],
            "vendor_id": vendor.json()["id"],
            "total_amount": 100,
        },
    )
    order_id = order.json()["id"]

    response = await async_client.patch(
        f"/api/v1/orders/{order_id}/status",
        headers=headers,
        json={"status": "DELIVERED"},
    )
    assert response.status_code == 422


async def test_create_order_with_unknown_customer_returns_404(async_client: AsyncClient):
    headers = await register_and_login(async_client)
    vendor = await async_client.post(
        "/api/v1/vendors",
        headers=headers,
        json={"name": "Widgets Inc", "contact_email": "v@w.com"},
    )

    response = await async_client.post(
        "/api/v1/orders",
        headers=headers,
        json={
            "customer_id": 999,
            "vendor_id": vendor.json()["id"],
            "total_amount": 100,
        },
    )
    assert response.status_code == 404
