from fastapi import APIRouter, Request

router = APIRouter()

@router.get("/health")
async def health_check():
    return {"status": "healthy"}

@router.get("/debug/routes")
async def list_routes(request: Request):
    routes = []
    for route in request.app.routes:
        routes.append({
            "path": route.path,
            "name": route.name,
            "methods": route.methods
        })
    return {"routes": routes}
