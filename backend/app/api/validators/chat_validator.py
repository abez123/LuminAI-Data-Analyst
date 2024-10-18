# app/api/validators/user.py

from pydantic import BaseModel


class AskQuestion(BaseModel):
    question: str

    class Config:
        # Use schema_extra for additional metadata in your API docs
        json_schema_extra = {
            "example": {
                "question": "write your question",
            }
        }
