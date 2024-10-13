from fastapi import APIRouter, Request
from app.api.controllers.data_pipeline_controller import (
    upload_spreadsheet
)

# Create an instance of APIRouter
data_pipeline_router = APIRouter()


@data_pipeline_router.post("/upload-spreadsheet")
async def upload():
    return upload_spreadsheet()   # Call the controller function

