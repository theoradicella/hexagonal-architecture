from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from adapters.driving.api.routes.auth import router as auth_router
from adapters.driving.api.routes.customers import router as customers_router
from adapters.driving.api.routes.orders import router as orders_router
from adapters.driving.api.routes.vendors import router as vendors_router
from infrastructure.config import settings


def create_app() -> FastAPI:
    application = FastAPI(title="Order Management API", version="0.1.0")

    application.add_middleware(
        CORSMiddleware,
        allow_origins=settings.CORS_ORIGINS,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    @application.get("/health")
    async def health() -> dict[str, str]:
        return {"status": "ok"}

    application.include_router(auth_router, prefix="/api/v1")
    application.include_router(customers_router, prefix="/api/v1")
    application.include_router(vendors_router, prefix="/api/v1")
    application.include_router(orders_router, prefix="/api/v1")

    return application


app = create_app()
