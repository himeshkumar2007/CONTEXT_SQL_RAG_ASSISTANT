import logging
import os
from datetime import datetime

import os
from dotenv import load_dotenv
load_dotenv()
LOG_FILE_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), '../../logs/app.log')




def get_db_config():
    return {
        "host": os.getenv("DB_HOST"),
        "user": os.getenv("DB_USER"),
        "password": os.getenv("DB_PASSWORD"),
        "database": os.getenv("DB_NAME"),
    }

# Configure logging
logging.basicConfig(
    filename=LOG_FILE_PATH,
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S"
)

def log_info(message: str):
    logging.info(message)
    print(f"[INFO] {datetime.now()} - {message}")  # Optional: print to console during development

def log_error(message: str):
    logging.error(message)
    print(f"[ERROR] {datetime.now()} - {message}")  # Optional: print to console during development

def clean_text(text: str) -> str:
    """
    Simple utility to clean input text (remove extra spaces, normalize line breaks, etc.)
    """
    if not text:
        return ""
    text = text.strip()
    text = ' '.join(text.split())
    return text
