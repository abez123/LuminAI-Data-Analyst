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

# Create the database tables


def init_db():
    try:
        logger.info("Creating database and tables...")
        # Use the Base defined at the top for creating tables
        Base.metadata.create_all(bind=db.engine)
        logger.info("Database and tables created successfully!")
    except Exception as e:
        logger.info(f"Error creating database: {e}")


def setup_database():
    try:
        # Try to create a session to check if the database exists
        db.execute_query("SELECT 1 FROM users LIMIT 1")
        logger.info("User found")
        # db.close()
    except OperationalError:
        # If the database doesn't exist, create it
        logger.info("Creating Database")
        init_db()


# Call setup_database at the module level
# if __name__ == "__main__": # Not working idk why
setup_database()
