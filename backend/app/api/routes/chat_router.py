from fastapi import APIRouter, Request
from app.api.controllers import chat_controller
from app.api.validators.chat_validator import AskQuestion

# Instance of APIRouter
chat_router = APIRouter()


@chat_router.post("/ask-question")
async def ask_question(body: AskQuestion):
    # if document
    # return
    # else
    return chat_controller.ask_question(body.question)


@chat_router.post("/get-conversactions")
async def get_conversactions():
    return chat_controller.get_convesactions()


@chat_router.post("/get-conversaction-history")
async def get_conversaction_history():
    return chat_controller.get_conversaction_history()
