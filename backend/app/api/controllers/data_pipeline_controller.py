from fastapi import UploadFile, HTTPException
from fastapi.responses import JSONResponse
from sqlalchemy.exc import SQLAlchemyError
from io import BytesIO
import pandas as pd
from app.config.logging_config import get_logger
from app.config.db_config import DB
from app.api.db.data_sources import DataSources
from app.utils.reader_utils import (pdf_to_document, text_to_document)
from app.config.db_config import VectorDB
import uuid

# Set up logging
logger = get_logger(__name__)
vector_db = VectorDB()


async def upload_spreadsheet(id: int, file: UploadFile, db: DB):
    buffer = None
    try:
        logger.info(f"Processing file: {file.filename}")
        session = db.create_session()
        # Validate file extension
        if not file.filename.lower().endswith(('.csv', '.xlsx', '.xls')):
            raise HTTPException(
                status_code=400, detail="Only CSV and Excel files are allowed")

        # Read file contents
        contents = await file.read()
        buffer = BytesIO(contents)

        # Determine file type and read accordingly
        if file.filename.lower().endswith('.csv'):
            df = pd.read_csv(buffer)
        else:
            df = pd.read_excel(buffer)

        # Generate a unique table name
        base_name = file.filename.rsplit('.', 1)[0].lower()
        table_name = f"{base_name}_{uuid.uuid4().hex[:8]}"

        # Insert data into database
        rows_affected = await db.insert_dataframe(df, table_name)

        # Create DataSources entry
        new_data_source = DataSources(
            name=file.filename,
            type='spreadsheet',
            table_name=table_name,
            user_id=id
        )

        session.add(new_data_source)
        session.commit()
        session.refresh(new_data_source)

        logger.info(f"Successfully processed file. Rows: {rows_affected}")

        return JSONResponse(status_code=201, content={
            "message": "Data uploaded successfully",
            "table_name": table_name,
            "rows_processed": rows_affected,
            "data_source_id": new_data_source.id
        })

    except HTTPException as he:
        raise he
    except SQLAlchemyError as e:
        logger.error(f"Database error: {str(e)}")
        raise HTTPException(status_code=500, detail="Database error occurred")
    except Exception as e:
        logger.error(f"Unexpected error: {str(e)}")
        raise HTTPException(
            status_code=500, detail="An unexpected error occurred")
    finally:
        if buffer:
            buffer.close()
        logger.info("Upload process completed")


async def upload_document(id: int, file: UploadFile, db: DB):
    buffer = None
    try:
        logger.info(f"Processing file: {file.filename}")
        session = db.create_session()
        vector_db.initialize_embedding()
        # Validate file extension
        if not file.filename.lower().endswith(('.pdf', '.doc', '.txt')):
            raise HTTPException(
                status_code=400, detail="Only Pdf, Doc and text files are allowed")

        # Generate a unique table name
        base_name = file.filename.rsplit('.', 1)[0].lower()
        table_name = f"{base_name}_{uuid.uuid4().hex[:8]}"

        # Read file contents
        contents = await file.read()
        buffer = BytesIO(contents)

        if file.filename.lower().endswith((".pdf")):
            documents = pdf_to_document(buffer, table_name)
        elif file.filename.lower().endswith(('.doc', '.txt')):
            documents = text_to_document(buffer, table_name)

        print(documents)
        vector_db.insert_data(documents, table_name)

        # Create DataSources entry
        new_data_source = DataSources(
            name=file.filename,
            type='document',
            table_name=table_name,
            user_id=id
        )

        session.add(new_data_source)
        session.commit()
        session.refresh(new_data_source)

        return JSONResponse(status_code=201, content={
            "message": "Data uploaded successfully",
            "table_name": table_name
        })

    except HTTPException as he:
        raise he
    except SQLAlchemyError as e:
        logger.error(f"Database error: {str(e)}")
        raise HTTPException(status_code=500, detail="Database error occurred")
    except Exception as e:
        logger.error(f"Unexpected error: {str(e)}")
        raise HTTPException(
            status_code=500, detail="An unexpected error occurred")
    finally:
        if buffer:
            buffer.close()
        logger.info("Upload process completed")


def connect_datasource():
    pass
