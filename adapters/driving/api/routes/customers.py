from fastapi import APIRouter, Depends, status

from adapters.driving.api.dependencies import get_current_user
from adapters.driving.api.schemas.customers import (
    CreateCustomerRequest,
    CustomerListResponse,
    CustomerResponse,
)
from domain.use_cases.customers.create_customer import CreateCustomerUseCase
from domain.use_cases.customers.list_customers import ListCustomersUseCase
from infrastructure.dependencies import (
    get_create_customer_use_case,
    get_list_customers_use_case,
)

router = APIRouter(
    prefix="/customers",
    tags=["customers"],
    dependencies=[Depends(get_current_user)],
)


@router.post(
    "",
    response_model=CustomerResponse,
    status_code=status.HTTP_201_CREATED,
)
async def create_customer(
    payload: CreateCustomerRequest,
    use_case: CreateCustomerUseCase = Depends(get_create_customer_use_case),
) -> CustomerResponse:
    customer = await use_case.execute(payload.name)
    assert customer.id is not None
    return CustomerResponse(
        id=customer.id,
        name=customer.name,
        created_at=customer.created_at,
    )


@router.get(
    "",
    response_model=CustomerListResponse,
)
async def list_customers(
    page: int = 1,
    page_size: int = 10,
    use_case: ListCustomersUseCase = Depends(get_list_customers_use_case),
) -> CustomerListResponse:
    customers = await use_case.execute(page=page, page_size=page_size)
    items = [
        CustomerResponse(id=c.id, name=c.name, created_at=c.created_at)
        for c in customers
        if c.id is not None
    ]
    return CustomerListResponse(
        items=items,
        total=len(items),
        page=page,
        page_size=page_size,
    )
