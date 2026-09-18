import os
from dotenv import load_dotenv

load_dotenv()

class Settings():
    
    GROQ_API_KEY = os.getenv("GROQ_API_KEY")
    MODEL_NAME = os.getenv("MODEL_NAME")
    TEMPERATURE = os.getenv("TEMPERATURE")
    MAX_RETRIES = os.getenv("MAX_RETRIES")

settings = Settings()