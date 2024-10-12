from fastapi import APIRouter
from app.api.controllers import auth_controller
from app.api.validators.auth_validators import (UserCreate, UserLogin)

# Create an instance of APIRouter
auth_router = APIRouter()


@auth_router.post("/signup")
async def signup(user: UserCreate):
    return auth_controller.signup(user)  # Call the controller function


@auth_router.get("/login")
async def login():
    return auth_controller.login()  # Call the controller function


@auth_router.get("/{userid}")
async def get_user():
    return auth_controller.get_user()  # Call the controller function
