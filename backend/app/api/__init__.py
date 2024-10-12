from fastapi import APIRouter
# Correct import of the hello router
from .routes.auth_router import auth_router

# Create the main API router
api_router = APIRouter()

# Include the hello router in the main API router
api_router.include_router(
    auth_router,
    prefix="/api/v1/user",
    tags=["user"],
)
