from fastapi import Depends, APIRouter, UploadFile, Request
from app.api.controllers.data_pipeline_controller import (
    upload_spreadsheet,
    upload_document,
    connect_datasource
)
from app.dependencies.database import get_db
from app.config.db_config import DB

# instance of APIRouter
data_pipeline_router = APIRouter()


@data_pipeline_router.post("/upload-spreadsheet")
async def upload_sheet(request: Request, file: UploadFile, db: DB = Depends(get_db)):
    user_id = request.state.user_id
    return await upload_spreadsheet(user_id, file, db)


@data_pipeline_router.post("/upload-document")
async def upload_doc(request: Request, file: UploadFile, db: DB = Depends(get_db)):
    user_id = request.state.user_id
    return await upload_document(user_id, file, db)


@data_pipeline_router.post("/get-data-source")
async def get_sources():
    return connect_datasource()


@data_pipeline_router.post("/get-source-tables")
async def get_source_tables():
    return connect_datasource()
