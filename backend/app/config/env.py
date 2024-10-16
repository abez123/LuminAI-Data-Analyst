# config.py
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Now you can access the variables
DATABASE_URL = os.getenv("DATABASE_URL")
SECRET_KEY = os.getenv("SECRET_KEY")
DEBUG = os.getenv("DEBUG")
GROQ_API_KEY = os.getenv("GROQ_API_KEY")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

# # Optionally, you can set default values if variables are not found
# DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./lumin.db")
# SECRET_KEY = os.getenv("SECRET_KEY", "defaultsecret")
