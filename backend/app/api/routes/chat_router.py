from fastapi import APIRouter, Request
from app.api.controllers import chat_controller
from app.api.validators.chat_validator import AskQuestion

# Create an instance of APIRouter
chat_router = APIRouter()


@chat_router.post("/ask-question")
async def ask_question(body: AskQuestion):
    # Call the controller function
    return chat_controller.ask_question(body.question)
