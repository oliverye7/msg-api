from fastapi import APIRouter
from app.api.v1.endpoints import health_router, auth_router

api_router = APIRouter()
api_router.include_router(health_router, tags=["health"])
api_router.include_router(auth_router, prefix="/auth", tags=["auth"])
