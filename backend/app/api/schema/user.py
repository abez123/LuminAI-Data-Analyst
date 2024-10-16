from sqlalchemy import Column, Integer, String
from sqlalchemy.exc import OperationalError
from sqlalchemy.ext.declarative import declarative_base
from app.config.db_config import DB
from app.config.env import DATABASE_URL
from app.config.logging_config import get_logger

logger = get_logger(__name__)

# Use the same Base for table creation
db = DB(DATABASE_URL)

Base = declarative_base()


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, autoincrement=True,
                index=True)  # Single primary key
    name = Column(String, index=True)  # Changed name to String
    email = Column(String, unique=True, index=True)
    hashed_password = Column(String)

