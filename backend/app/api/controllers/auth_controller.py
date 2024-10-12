from fastapi import HTTPException
from fastapi.responses import JSONResponse
from sqlalchemy import select
from sqlalchemy.exc import SQLAlchemyError
from app.api.schema.user import User
from app.config.db_config import DB
from app.config.env import DATABASE_URL
from app.api.validators.auth_validators import (UserCreate, UserLogin)
from app.utils.auth_utils import (get_password_hash)
from app.config.logging_config import get_logger

logger = get_logger(__name__)

db = DB(DATABASE_URL)
session = db.create_session()


def signup(user: UserCreate):
    try:
        # Check if the user already exists
        find_query = select(User).where(User.email == user.email)
        existing_user = session.scalars(find_query).one_or_none()
        logger.info("existing_user :", existing_user)
        if existing_user:
            raise HTTPException(
                status_code=400, detail="Email already registered")

        # Insert the new user
        user_instance = User(
            name=user.name,
            email=user.email,
            hashed_password=get_password_hash(user.password)
        )

        session.add(user_instance)
        session.commit()

        # Return a success response
        return JSONResponse(status_code=201, content={
            "message": "User created successfully"
        })

    except SQLAlchemyError as e:
        # Catch SQL-related errors and raise HTTP exception
        raise HTTPException(
            status_code=500, detail="Database error: " + str(e))

    except Exception as e:
        # Catch all other errors and raise HTTP exception
        raise HTTPException(
            status_code=500, detail="Something went wrong: " + str(e))


def login(user: UserLogin):
    return {"message": "Login user"}


def get_user():
    return {"message": "Get user"}
