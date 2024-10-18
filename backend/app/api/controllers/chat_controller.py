from fastapi.responses import JSONResponse
from app.utils.chat_utils import (execute_workflow, execute_document_chat)
from app.api.validators.chat_validator import AskQuestion
from app.config.db_config import DB


async def ask_question(id: int, body: AskQuestion, db: DB):
    try:

        if body.type == "url" or body.type == "spreadsheet":
            print("execure_workflow")
            # return execure_workflow()
        else:
            print("execure_document_chat")
            return execute_document_chat(
                body.question, "text-embedding-3-large", "speech_81a36223")

    except Exception as e:
        # Catch all other errors and raise HTTP exception
        return JSONResponse(status_code=500, content={
            "message": "Something went wrong",
            "error": str(e)
        })


def get_convesactions():
    pass


def get_conversaction_history():
    pass
