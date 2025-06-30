import logging
import os

# Create logs directory if not exists
os.makedirs("logs", exist_ok=True)

# Set up logging
logging.basicConfig(
    filename="logs/app.log",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
)

def log_info(message: str):
    logging.info(message)

def log_error(message: str):
    logging.error(message)
