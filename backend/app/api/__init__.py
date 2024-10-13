from fastapi import APIRouter
# Correct import of the hello router
from .routes.auth_router import auth_router
from .routes.data_pipeline_router import data_pipeline_router
from .routes.chat_router import chat_router

# Create the main API router
api_router = APIRouter()

# Include the hello router in the main API router
api_router.include_router(
    auth_router,
    prefix="/api/v1/user",
    tags=["user"],
)

api_router.include_router(
    data_pipeline_router,
    prefix="/api/v1/data",
    tags=["data"],
)

api_router.include_router(
    chat_router,
    prefix="/api/v1/chat",
    tags=["chat"],
)
