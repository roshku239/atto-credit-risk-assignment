import logging
from logging.handlers import RotatingFileHandler
from pathlib import Path

# Base directories
BASE_DIR = Path(__file__).resolve().parents[1]
LOG_DIR = BASE_DIR / "logs"
LOG_DIR.mkdir(exist_ok=True)

LOG_FILE = LOG_DIR / "etl.log"


def get_logger(name: str) -> logging.Logger:
    
    # Create and configure a logger to ensure consistent logging across all ETL modules.
    logger = logging.getLogger(name)
    logger.setLevel(logging.INFO)

    # Avoid duplicate handlers in interactive sessions
    if logger.handlers:
        return logger

    
    # Console Handler  
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.INFO)

    console_format = logging.Formatter(
        fmt="%(asctime)s | %(levelname)s | %(name)s | %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )
    console_handler.setFormatter(console_format)
    # File Handler (rotating)

    file_handler = RotatingFileHandler(
        LOG_FILE, maxBytes=2_000_000, backupCount=3
    )
    file_handler.setLevel(logging.INFO)

    file_format = logging.Formatter(
        fmt="%(asctime)s | %(levelname)s | %(name)s | %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )
    file_handler.setFormatter(file_format)

    # Attach handlers
    logger.addHandler(console_handler)
    logger.addHandler(file_handler)

    return logger
