from typing import List, Dict
from sqlalchemy import create_engine, inspect, text
from sqlalchemy.orm import sessionmaker, Session
from app.config.logging_config import get_logger

logger = get_logger(__name__)


class DB:
    def __init__(self, db_url: str):
        """
        Initialize the database connection.

        Args:
            db_url (str): Database URL
        """
        self.engine = create_engine(db_url)
        self.session = sessionmaker(autocommit=False, autoflush=False, bind=self.engine)

    def execute_query(self, query: str) -> list:
        print("======== execute_query ========")
        with self.session() as session:
            result = session.execute(text(query))
            # return result
            if result.returns_rows:
                # Convert RowProxy to dict
                return [row for row in result.fetchall()]
            else:
                # For non-SELECT queries, commit the transaction and return an empty list
                session.commit()
                return []

    def create_session(self) -> Session:
        """
        Create a new database session.

        Returns:
            Session: Database session
        """
        return self.session()

    def get_schemas(self, table_names: List[str]) -> List[Dict]:
        try:
            # Create an inspector object
            inspector = inspect(self.engine)

            # Initialize an array to hold the schema information for all tables
            schemas_info = []

            for table_name in table_names:
                schema_info = {
                    "table_name": table_name,
                    "schema": []
                }

                # Get the columns for the specified table
                columns = inspector.get_columns(table_name)
                # Collect column information
                for column in columns:
                    schema_info["schema"].append({
                        "name": column['name'],
                        "type": str(column['type']),
                        "nullable": column['nullable']
                    })

                # Append the schema information for the current table to the list
                schemas_info.append(schema_info)

            # Return the schema information for all tables
            return schemas_info

        except Exception as e:
            logger.error(f"An error occurred: {e}")
            return []  # Return an empty list in case of an error
