from pydantic import BaseModel, Field
from typing import List, Optional


class AskQuestion(BaseModel):
    question: str = Field(...,
                          description="The question you want to ask about the data")
    type: str = Field(..., description="The type of question or analysis")
    selected_tables: Optional[List[str]] = Field(
        None, description="List of selected tables (optional)")
    dataset_id: int = Field(..., description="Dataset ID to query")

    class Config:
        json_schema_extra = {
            "example": {
                "question": "What is the total revenue for each product category?",
                "type": "url",
                "selected_tables": ["sales", "products"],
                "dataset_id": "123"
            }
        }
