from fastapi import APIRouter, Depends, HTTPException, status

from adapters.driving.api.dependencies import get_current_user
from adapters.driving.api.schemas.orders import (
    CreateOrderRequest,
    OrderListResponse,
    OrderResponse,
    TransitionStatusRequest,
)
from domain.entities.order import Order, OrderStatus
from domain.exceptions import (
    CustomerNotFoundError,
    InvalidStatusTransitionError,
    OrderNotFoundError,
    VendorNotFoundError,
)
from domain.use_cases.orders.cancel_order import CancelOrderUseCase
from domain.use_cases.orders.create_order import CreateOrderUseCase
from domain.use_cases.orders.list_orders import ListOrdersUseCase
from domain.use_cases.orders.transition_order_status import TransitionOrderStatusUseCase
from infrastructure.dependencies import (
    get_cancel_order_use_case,
    get_create_order_use_case,
    get_list_orders_use_case,
    get_transition_order_status_use_case,
)

router = APIRouter(
    prefix="/orders",
    tags=["orders"],
    dependencies=[Depends(get_current_user)],
)


def _to_response(order: Order) -> OrderResponse:
    assert order.id is not None
    return OrderResponse(
        id=order.id,
        customer_id=order.customer_id,
        vendor_id=order.vendor_id,
        status=order.status,
        total_amount=order.total_amount,
        created_at=order.created_at,
    )


@router.post(
    "",
    response_model=OrderResponse,
    status_code=status.HTTP_201_CREATED,
)
async def create_order(
    payload: CreateOrderRequest,
    use_case: CreateOrderUseCase = Depends(get_create_order_use_case),
) -> OrderResponse:
    try:
        order = await use_case.execute(
            customer_id=payload.customer_id,
            vendor_id=payload.vendor_id,
            total_amount=payload.total_amount,
        )
    except (CustomerNotFoundError, VendorNotFoundError) as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))

    return _to_response(order)


@router.get("", response_model=OrderListResponse)
async def list_orders(
    page: int = 1,
    page_size: int = 10,
    status_filter: OrderStatus | None = None,
    customer_id: int | None = None,
    vendor_id: int | None = None,
    use_case: ListOrdersUseCase = Depends(get_list_orders_use_case),
) -> OrderListResponse:
    orders = await use_case.execute(
        page=page,
        page_size=page_size,
        status=status_filter,
        customer_id=customer_id,
        vendor_id=vendor_id,
    )
    items = [_to_response(o) for o in orders]
    return OrderListResponse(
        items=items,
        total=len(items),
        page=page,
        page_size=page_size,
    )


@router.patch("/{order_id}/status", response_model=OrderResponse)
async def transition_status(
    order_id: int,
    payload: TransitionStatusRequest,
    use_case: TransitionOrderStatusUseCase = Depends(get_transition_order_status_use_case),
) -> OrderResponse:
    try:
        order = await use_case.execute(order_id=order_id, new_status=payload.status)
    except OrderNotFoundError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
    except InvalidStatusTransitionError as e:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail=str(e),
        )

    return _to_response(order)


@router.delete("/{order_id}", response_model=OrderResponse)
async def cancel_order(
    order_id: int,
    use_case: CancelOrderUseCase = Depends(get_cancel_order_use_case),
) -> OrderResponse:
    try:
        order = await use_case.execute(order_id=order_id)
    except OrderNotFoundError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
    except InvalidStatusTransitionError as e:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail=str(e),
        )

    return _to_response(order)
