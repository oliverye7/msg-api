from fastapi import APIRouter
from app.api.v1.endpoints import health_router, auth_router
from app.api.v1.endpoints.analytics import router as analytics_router

api_router = APIRouter()
api_router.include_router(health_router, tags=["health"])
api_router.include_router(auth_router, prefix="/auth", tags=["auth"])
api_router.include_router(analytics_router, prefix="/analytics", tags=["analytics"])
