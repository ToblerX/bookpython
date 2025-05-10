from dotenv import load_dotenv
import os
from passlib.context import CryptContext
from fastapi.security import OAuth2PasswordBearer

load_dotenv()

# DATABASE INITIALIZATION
DATABASE_URL = os.getenv("DATABASE_URL")
GENRES = [
    "Fiction",
    "Non-fiction",
    "Mystery",
    "Fantasy",
    "Science Fiction",
    "Romance",
    "Historical Fiction",
    "Biography",
    "Horror",
    "Young Adult",
    "Children’s Literature",
    "Self-Help",
    "Graphic Novels",
    "Poetry",
    "Classics",
    "Adventure",
    "Literary Fiction",
    "Religion",
    "Science",
    "Travel",
]
ADMIN_PASSWORD = os.getenv("ADMIN_PASSWORD")

# IMAGE PATHS
IMAGES_BOOKS_PATH = "app/static/images/books/"
DEFAULT_COVER_PATH = IMAGES_BOOKS_PATH + "cover_not_available.jpg"

# USERS AUTH
PWD_CONTEXT = CryptContext(schemes=["bcrypt"], deprecated="auto")
SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")
