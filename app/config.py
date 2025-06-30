import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Gemini / Google API
GOOGLE_API_KEY = os.getenv("GEMINI_API_KEY")

# Pinecone configuration
PINECONE_API_KEY = os.getenv("PINECONE_API_KEY")
PINECONE_INDEX_NAME = os.getenv("PINECONE_INDEX_NAME", "vector-transform")

# Database configuration
DB_HOST = os.getenv("DB_HOST")
DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_NAME = os.getenv("DB_NAME")

# Any other config constants can go here
