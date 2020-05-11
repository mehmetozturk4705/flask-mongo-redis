import os
from dotenv import load_dotenv
load_dotenv()
from datetime import timedelta

BASE_PATH = os.path.dirname(os.path.dirname(__file__))

MONGODB_SETTINGS = {
    "db": os.getenv("MONGODB_DBNAME"),
    "host": os.getenv("MONGODB_HOST"),
    "username": os.getenv("MONGODB_USER"),
    "password": os.getenv("MONGODB_PASSWORD")
}

CACHE_REDIS_HOST=os.getenv("CACHE_REDIS_HOST")
CACHE_REDIS_PORT=os.getenv("CACHE_REDIS_PORT")
CACHE_TIMEOUT=60*5 #5 minutes

JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY")
JWT_TIMEOUT = timedelta(minutes=20)