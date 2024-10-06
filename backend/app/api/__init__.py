from fastapi import APIRouter

# Initialize the main API router
api_router = APIRouter()

# Import and include submodules (routes)
from .routes import api_router as routes_router

# Include route modules in the main API router
api_router.include_router(routes_router)