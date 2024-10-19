from fastapi import HTTPException
from fastapi.responses import JSONResponse
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy import select
from app.utils.chat_utils import (execute_workflow, execute_document_chat)
from app.api.validators.chat_validator import AskQuestion, InitiateCinversaction
from app.config.db_config import DB
from app.config.logging_config import get_logger
from app.api.db.data_sources import DataSources

# Set up logging
logger = get_logger(__name__)


async def ask_question(id: int, body: AskQuestion, db: DB):
    try:
        with db.session() as session:
            data_source = session.execute(select(DataSources).where(
                DataSources.id == id)).scalar_one_or_none()

        if body.type == "url":
            return execute_workflow(
                question=body.question,
                db_url=data_source.connection_url,
                table_list=body.selected_tables
            )
        elif body.type == "spreadsheet":
            return execute_workflow(
                question=body.question,
                db=db,
                table_list=[data_source.table_name]
            )
        else:
            print("execure_document_chat")
            return execute_document_chat(
                body.question, "text-embedding-3-large", "speech_81a36223")

    except HTTPException as he:
        return JSONResponse(status_code=500, content={
            "message": "Something went wrong",
            "error": str(he)
        })
    except SQLAlchemyError as e:
        logger.error(f"Database error: {str(e)}")
        return JSONResponse(status_code=500, content={
            "message": "Database error occurred",
            "error": str(e)
        })
    except Exception as e:
        # Catch all other errors and raise HTTP exception
        logger.error(f"Something went wrong: {str(e)}")
        return JSONResponse(status_code=500, content={
            "message": "Something went wrong",
            "error": str(e)
        })


def initiate_convesactions(user_id: int, body: InitiateCinversaction, db: DB):
    pass


def get_convesactions():
    pass


def get_conversaction_history():
    pass
