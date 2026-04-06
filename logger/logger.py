import logging
import os
LOG_LEVEL = os.getenv("LOG_LEVEL", "DEBUG")
from logging.handlers import RotatingFileHandler
LOG_DIR = "app/logs/files"

if not os.path.exists(LOG_DIR):
    os.makedirs(LOG_DIR)

def get_logger(name):
    logger = logging.getLogger(name)
    
    if logger.handlers:
        return logger
    
    logger.setLevel(LOG_LEVEL)

    formatter = logging.Formatter(
        "%(asctime)s | %(levelname)s | %(name)s | %(message)s"
    )

    debug_handler = RotatingFileHandler(
        f"{LOG_DIR}/debug.log",
        maxBytes=2*1024*1024,
        backupCount=3
    )

    debug_handler.setLevel(logging.DEBUG)
    debug_handler.setFormatter(formatter)

    error_handler = RotatingFileHandler(
        f"{LOG_DIR}/exception.log",
        maxBytes=2*1024*1024,
        backupCount=3
    )

    error_handler.setLevel(logging.ERROR)
    error_handler.setFormatter(formatter)

    console_handler = logging.StreamHandler()
    console_handler.setFormatter(formatter)
    console_handler.setLevel(logging.INFO)

    logger.addHandler(debug_handler)
    logger.addHandler(error_handler)
    logger.addHandler(console_handler)
    logger.propagate = False

    return logger

