import logging


# Yes, info, warning, and error are logging levels.
logger = logging.getLogger(__name__)  # __name__ is the scope of this logger which is this module
logger.setLevel(logging.INFO)             # Set level for logger
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s') # Set format for log messages

# Create a console handler with INFO level
console_handler = logging.StreamHandler()
console_handler.setLevel(logging.INFO)
console_handler.setFormatter(formatter)
logger.addHandler(console_handler)


file_handler = logging.FileHandler('app.log')
file_handler.setLevel(logging.INFO)
file_handler.setFormatter(formatter)
logger.addHandler(file_handler)


logger.info("Server started")
logger.warning("Token is about to expire")
logger.error("Database connection failed")


# python3 -m src.debug

