from fastapi import HTTPException
from fastapi.responses import JSONResponse
from sqlalchemy import select
from sqlalchemy.exc import SQLAlchemyError
from app.api.schema.user import User
from app.config.db_config import DB
from app.config.env import DATABASE_URL
from app.api.validators.auth_validators import (UserCreate, UserLogin)
from app.utils.auth_utils import (get_password_hash,verify_password,create_access_token)
from app.config.logging_config import get_logger

logger = get_logger(__name__)

db = DB(DATABASE_URL)
session = db.create_session()


def signup(user: UserCreate):
    try:
        # Check if the user already exists
        find_query = select(User).where(User.email == user.email)
        existing_user = session.scalars(find_query).one_or_none()
        if existing_user:
            return JSONResponse(status_code=400, content={
                "message": "Email already registered"
            })

        # Insert the new user
        user_instance = User(
            name=user.name,
            email=user.email,
            hashed_password=get_password_hash(user.password)
        )

        session.add(user_instance)
        session.commit()

                # Generate JWT token for the new user
        token_data = {
            "id": user_instance.id
        }
        access_token = create_access_token(data=token_data)


        # Return a success response
        return JSONResponse(status_code=201, content={
            "message": "User created successfully",
            "user_id": user_instance.id,
            "access_token": access_token,
        })

    except SQLAlchemyError as e:
        # Catch SQL-related errors and raise HTTP exception
        return JSONResponse(status_code=500, content={
            "message": "Database error",
            "error": str(e)
        })
    
    except Exception as e:
        # Catch all other errors and raise HTTP exception
        return JSONResponse(status_code=500, content={
            "message": "Something went wrong",
            "error": str(e)
        })


def login(user: UserLogin):
    try:
        # Find the user by email
        find_query = select(User).where(User.email == user.email)
        db_user = session.scalars(find_query).one_or_none()

        # If user does not exist
        if not db_user:
            raise HTTPException(status_code=400, detail="Invalid credentials")

        # Verify password
        if not verify_password(user.password, db_user.hashed_password):
            raise HTTPException(status_code=400, detail="Invalid credentials")

        # Generate JWT token
        token_data = {"id": db_user.id}
        access_token = create_access_token(data=token_data)

        # Return success response with the token
        return JSONResponse(status_code=200, content={
            "message": "Login successful",
            "user_id": db_user.id,
            "access_token": access_token
        })

    except SQLAlchemyError as e:
        # Catch SQL-related errors and raise HTTP exception
        return JSONResponse(status_code=500, content={
            "message": "Database error",
            "error": str(e)
        })
    
    except Exception as e:
        # Catch all other errors and raise HTTP exception
        return JSONResponse(status_code=500, content={
            "message": "Something went wrong",
            "error": str(e)
        })


def get_user(id: int):
    try:
        # Fetch the user from the database using the email
        find_query = select(User).where(User.id == id)
        db_user = session.scalars(find_query).one_or_none()

        if not db_user:
            return JSONResponse(status_code=404, content={
                "message": "User not found",
                "error": str(e)
            })

        # Return the user
        return JSONResponse(status_code=200, content={
            "id": db_user.id,
            "name": db_user.name,
            "email": db_user.email
        })

    except SQLAlchemyError as e:
        # Catch SQL-related errors and raise HTTP exception
        return JSONResponse(status_code=500, content={
            "message": "Database error",
            "error": str(e)
        })
    
    except Exception as e:
        # Catch all other errors and raise HTTP exception
        return JSONResponse(status_code=500, content={
            "message": "Something went wrong",
            "error": str(e)
        })
