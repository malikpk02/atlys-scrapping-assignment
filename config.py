import os

from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Access the environment variables
SCRAPPING_BASE_URL = os.getenv("SCRAPPING_BASE_URL")
DEFAULT_HEADERS = os.getenv("DEFAULT_HEADERS")
API_TIMEOUT = int(os.getenv("API_TIMEOUT"))
STATIC_TOKEN = os.getenv("STATIC_TOKEN")
REDIS_HOST = os.getenv("REDIS_HOST")
REDIS_PORT = int(os.getenv("REDIS_PORT"))
