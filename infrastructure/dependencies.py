from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from adapters.driven.auth.bcrypt_password_hasher import BcryptPasswordHasher
from adapters.driven.auth.jwt_token_service import JwtTokenService
from adapters.driven.notifications.smtp_email_notifier import SmtpEmailNotifier
from adapters.driven.persistence.customer_repository import SqlAlchemyCustomerRepository
from adapters.driven.persistence.order_repository import SqlAlchemyOrderRepository
from adapters.driven.persistence.user_repository import SqlAlchemyUserRepository
from adapters.driven.persistence.vendor_repository import SqlAlchemyVendorRepository
from domain.ports.customer_repository import ICustomerRepository
from domain.ports.email_notifier import IEmailNotifier
from domain.ports.order_repository import IOrderRepository
from domain.ports.password_hasher import IPasswordHasher
from domain.ports.token_service import ITokenService
from domain.ports.user_repository import IUserRepository
from domain.ports.vendor_repository import IVendorRepository
from domain.use_cases.auth.login import LoginUseCase
from domain.use_cases.auth.register import RegisterUseCase
from domain.use_cases.customers.create_customer import CreateCustomerUseCase
from domain.use_cases.customers.list_customers import ListCustomersUseCase
from domain.use_cases.orders.cancel_order import CancelOrderUseCase
from domain.use_cases.orders.create_order import CreateOrderUseCase
from domain.use_cases.orders.list_orders import ListOrdersUseCase
from domain.use_cases.orders.transition_order_status import TransitionOrderStatusUseCase
from domain.use_cases.vendors.create_vendor import CreateVendorUseCase
from domain.use_cases.vendors.list_vendors import ListVendorsUseCase
from infrastructure.config import settings
from infrastructure.database import get_session


# Repositories
def get_user_repository(
    session: AsyncSession = Depends(get_session),
) -> IUserRepository:
    return SqlAlchemyUserRepository(session)


def get_customer_repository(
    session: AsyncSession = Depends(get_session),
) -> ICustomerRepository:
    return SqlAlchemyCustomerRepository(session)


def get_vendor_repository(
    session: AsyncSession = Depends(get_session),
) -> IVendorRepository:
    return SqlAlchemyVendorRepository(session)


def get_order_repository(
    session: AsyncSession = Depends(get_session),
) -> IOrderRepository:
    return SqlAlchemyOrderRepository(session)


# Services
def get_password_hasher() -> IPasswordHasher:
    return BcryptPasswordHasher()


def get_token_service() -> ITokenService:
    return JwtTokenService(
        secret_key=settings.SECRET_KEY,
        algorithm=settings.ALGORITHM,
        expire_minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES,
    )


def get_email_notifier() -> IEmailNotifier:
    return SmtpEmailNotifier(
        host="smtp.example.com",
        port=587,
        username="noreply@example.com",
        password="changeme",
    )


# Auth use cases
def get_register_use_case(
    user_repo: IUserRepository = Depends(get_user_repository),
    password_hasher: IPasswordHasher = Depends(get_password_hasher),
) -> RegisterUseCase:
    return RegisterUseCase(user_repo, password_hasher)


def get_login_use_case(
    user_repo: IUserRepository = Depends(get_user_repository),
    token_service: ITokenService = Depends(get_token_service),
    password_hasher: IPasswordHasher = Depends(get_password_hasher),
) -> LoginUseCase:
    return LoginUseCase(user_repo, token_service, password_hasher)


# Customer use cases
def get_create_customer_use_case(
    customer_repo: ICustomerRepository = Depends(get_customer_repository),
) -> CreateCustomerUseCase:
    return CreateCustomerUseCase(customer_repo)


def get_list_customers_use_case(
    customer_repo: ICustomerRepository = Depends(get_customer_repository),
) -> ListCustomersUseCase:
    return ListCustomersUseCase(customer_repo)


# Vendor use cases
def get_create_vendor_use_case(
    vendor_repo: IVendorRepository = Depends(get_vendor_repository),
) -> CreateVendorUseCase:
    return CreateVendorUseCase(vendor_repo)


def get_list_vendors_use_case(
    vendor_repo: IVendorRepository = Depends(get_vendor_repository),
) -> ListVendorsUseCase:
    return ListVendorsUseCase(vendor_repo)


# Order use cases
def get_create_order_use_case(
    order_repo: IOrderRepository = Depends(get_order_repository),
    customer_repo: ICustomerRepository = Depends(get_customer_repository),
    vendor_repo: IVendorRepository = Depends(get_vendor_repository),
) -> CreateOrderUseCase:
    return CreateOrderUseCase(order_repo, customer_repo, vendor_repo)


def get_list_orders_use_case(
    order_repo: IOrderRepository = Depends(get_order_repository),
) -> ListOrdersUseCase:
    return ListOrdersUseCase(order_repo)


def get_transition_order_status_use_case(
    order_repo: IOrderRepository = Depends(get_order_repository),
) -> TransitionOrderStatusUseCase:
    return TransitionOrderStatusUseCase(order_repo)


def get_cancel_order_use_case(
    order_repo: IOrderRepository = Depends(get_order_repository),
) -> CancelOrderUseCase:
    return CancelOrderUseCase(order_repo)
