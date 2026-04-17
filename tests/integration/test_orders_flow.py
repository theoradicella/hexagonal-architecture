from httpx import AsyncClient

from tests.integration._helpers import register_and_login


async def _seed_customer_and_vendor(
    client: AsyncClient, headers: dict[str, str]
) -> tuple[int, int]:
    customer = await client.post(
        "/api/v1/customers",
        headers=headers,
        json={"name": "Acme Corp"},
    )
    vendor = await client.post(
        "/api/v1/vendors",
        headers=headers,
        json={"name": "Widgets Inc", "contact_email": "v@w.com"},
    )
    return customer.json()["id"], vendor.json()["id"]


async def test_full_order_lifecycle(async_client: AsyncClient):
    headers = await register_and_login(async_client)
    customer_id, vendor_id = await _seed_customer_and_vendor(async_client, headers)

    create = await async_client.post(
        "/api/v1/orders",
        headers=headers,
        json={
            "customer_id": customer_id,
            "vendor_id": vendor_id,
            "total_amount": 500,
        },
    )
    assert create.status_code == 201
    order = create.json()
    assert order["status"] == "PENDING"

    confirm = await async_client.patch(
        f"/api/v1/orders/{order['id']}/status",
        headers=headers,
        json={"status": "CONFIRMED"},
    )
    assert confirm.status_code == 200
    assert confirm.json()["status"] == "CONFIRMED"

    cancel = await async_client.delete(
        f"/api/v1/orders/{order['id']}",
        headers=headers,
    )
    assert cancel.status_code == 200
    assert cancel.json()["status"] == "CANCELLED"


async def test_list_orders_filters_by_status(async_client: AsyncClient):
    headers = await register_and_login(async_client)
    customer_id, vendor_id = await _seed_customer_and_vendor(async_client, headers)

    for _ in range(3):
        await async_client.post(
            "/api/v1/orders",
            headers=headers,
            json={
                "customer_id": customer_id,
                "vendor_id": vendor_id,
                "total_amount": 100,
            },
        )

    first_order_id = 1
    await async_client.patch(
        f"/api/v1/orders/{first_order_id}/status",
        headers=headers,
        json={"status": "CONFIRMED"},
    )

    confirmed = await async_client.get(
        "/api/v1/orders?status_filter=CONFIRMED",
        headers=headers,
    )
    assert confirmed.status_code == 200
    items = confirmed.json()["items"]
    assert len(items) == 1
    assert items[0]["status"] == "CONFIRMED"
