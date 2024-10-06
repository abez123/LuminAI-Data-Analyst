import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    MODEL_PATH = os.getenv("MODEL_PATH", "./models")
    API_KEY = os.getenv("API_KEY", "your-openai-api-key")
