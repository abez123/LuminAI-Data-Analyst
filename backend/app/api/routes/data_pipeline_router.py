from fastapi import Depends, APIRouter, UploadFile, Request
from app.api.controllers.data_pipeline_controller import (
    upload_spreadsheet,
    upload_document,
    connect_datasource
)
from app.dependencies.database import get_db
from app.config.db_config import DB

# Create an instance of APIRouter
data_pipeline_router = APIRouter()


@data_pipeline_router.post("/upload-spreadsheet")
async def upload_sheet(request: Request, file: UploadFile, db: DB = Depends(get_db)):
    user_id = request.state.user_id
    # Call the controller function  nn
    return await upload_spreadsheet(user_id, file, db)


@data_pipeline_router.post("/upload-document")
async def upload_doc():
    return upload_document()   # Call the controller function


@data_pipeline_router.post("/add-data-source")
async def upload_doc():
    return connect_datasource()   # Call the controller function
