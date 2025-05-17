from dotenv import load_dotenv
import os

from itsdangerous import URLSafeTimedSerializer
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

# EMAIL CONFIGURATION
MAIL_USERNAME = os.getenv("MAIL_USERNAME")
MAIL_PASSWORD = os.getenv("MAIL_PASSWORD")
MAIL_FROM = os.getenv("MAIL_FROM")
MAIL_PORT = os.getenv("MAIL_PORT")
MAIL_SERVER = os.getenv("MAIL_SERVER")
MAIL_FROM_NAME = os.getenv("MAIL_FROM_NAME")
MAIL_STARTTLS = True
MAIL_SSL_TLS = False
USE_CREDENTIALS = True
VALIDATE_CERTS = True

# EMAIL VERIFICATION
serializer = URLSafeTimedSerializer(secret_key=SECRET_KEY, salt="email-configuration")
DOMAIN = os.getenv("DOMAIN")

# LENGTH VALIDATION PARAMETERS
BOOK_NAME_MIN = 3
BOOK_NAME_MAX = 70
BOOK_DESC_MIN = 100
BOOK_DESC_MAX = 500
GENRE_NAME_MIN = 3
GENRE_NAME_MAX = 30
USERNAME_MIN = 3
USERNAME_MAX = 15
PASSWORD_MIN = 8
PASSWORD_MAX = 16