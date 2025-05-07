from dotenv import load_dotenv
import os

load_dotenv()
DATABASE_URL = os.getenv("DATABASE_URL")
SECRET_KEY = os.getenv("SECRET_KEY")
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
