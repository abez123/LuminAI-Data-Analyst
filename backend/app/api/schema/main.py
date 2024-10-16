from sqlalchemy import create_engine, MetaData, Table, Column, Integer, String, Enum
from app.config.env import DATABASE_URL

# Create the SQLAlchemy engine
engine = create_engine(DATABASE_URL)

# Create a metadata object
meta = MetaData()

# Define the table structure
users_table = Table(
    "users",
    meta,
    Column("id", Integer, primary_key=True, autoincrement=True),
    Column("name", String(50)),
    Column("email", String(100), unique=True),
    Column("hashed_password", String(400), unique=True),
)

# Define an Enum type for 'type' column
type_enum = Enum('document', 'url', name='type_enum')
data_sources_table = Table(
    "data_sources",
    meta,
    Column("id", Integer, primary_key=True, autoincrement=True),
    Column("name", String(50)),
    Column("type", type_enum),
    Column("connection_url", String(400), unique=True),
)

def create_tables():
    try:
        # Create the table
        meta.create_all(engine)
        print("Table created successfully!")
    except Exception as e:
        print(f"Error creating table: {e}")