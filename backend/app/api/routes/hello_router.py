# backend/app/api/routes/hello_router.py

from fastapi import APIRouter
from app.api.controllers import hello_controller

# Create an instance of APIRouter
hello_router = APIRouter()

# Define the /hello endpoint
@hello_router.get("/hello")
def hello():
    return hello_controller.hello_world()  # Call the controller function
