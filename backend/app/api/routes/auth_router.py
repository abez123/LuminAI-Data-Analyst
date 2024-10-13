from fastapi import APIRouter, Request
from app.api.controllers import auth_controller
from app.api.validators.auth_validators import (UserCreate, UserLogin)

# Create an instance of APIRouter
auth_router = APIRouter()


@auth_router.post("/signup")
async def signup(user: UserCreate):
    return auth_controller.signup(user)  # Call the controller function


@auth_router.post("/login")
async def login(user: UserLogin):
    return auth_controller.login(user)  # Call the controller function


@auth_router.get("/")
async def get_user(request: Request):
    user_id = request.state.user_id
    return auth_controller.get_user(user_id)  # Call the controller function
