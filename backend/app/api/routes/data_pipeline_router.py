from fastapi import APIRouter, Request
from app.api.controllers.data_pipeline_controller import (
    upload_spreadsheet,
    upload_document
)

# Create an instance of APIRouter
data_pipeline_router = APIRouter()


@data_pipeline_router.post("/upload-spreadsheet")
async def upload_sheet():
    return upload_spreadsheet()   # Call the controller function


@data_pipeline_router.post("/upload-document")
async def upload_doc():
    return upload_document()   # Call the controller function
