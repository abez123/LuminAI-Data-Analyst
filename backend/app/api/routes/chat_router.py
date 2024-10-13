from fastapi import APIRouter, Request
from app.api.controllers import chat_controller

# Create an instance of APIRouter
chat_router = APIRouter()

@chat_router.get("/ask-question")
async def ask_question():
    return chat_controller.ask_question()   # Call the controller function

