from fastapi import APIRouter, Depends, status

from adapters.driving.api.dependencies import get_current_user
from adapters.driving.api.schemas.vendors import (
    CreateVendorRequest,
    VendorListResponse,
    VendorResponse,
)
from domain.use_cases.vendors.create_vendor import CreateVendorUseCase
from domain.use_cases.vendors.list_vendors import ListVendorsUseCase
from infrastructure.dependencies import (
    get_create_vendor_use_case,
    get_list_vendors_use_case,
)

router = APIRouter(
    prefix="/vendors",
    tags=["vendors"],
    dependencies=[Depends(get_current_user)],
)


@router.post(
    "",
    response_model=VendorResponse,
    status_code=status.HTTP_201_CREATED,
)
async def create_vendor(
    payload: CreateVendorRequest,
    use_case: CreateVendorUseCase = Depends(get_create_vendor_use_case),
) -> VendorResponse:
    vendor = await use_case.execute(payload.name, payload.contact_email)
    assert vendor.id is not None
    return VendorResponse(
        id=vendor.id,
        name=vendor.name,
        contact_email=vendor.contact_email,
        created_at=vendor.created_at,
    )


@router.get(
    "",
    response_model=VendorListResponse,
)
async def list_vendors(
    page: int = 1,
    page_size: int = 10,
    use_case: ListVendorsUseCase = Depends(get_list_vendors_use_case),
) -> VendorListResponse:
    vendors = await use_case.execute(page=page, page_size=page_size)
    items = [
        VendorResponse(
            id=v.id,
            name=v.name,
            contact_email=v.contact_email,
            created_at=v.created_at,
        )
        for v in vendors
        if v.id is not None
    ]
    return VendorListResponse(
        items=items,
        total=len(items),
        page=page,
        page_size=page_size,
    )
