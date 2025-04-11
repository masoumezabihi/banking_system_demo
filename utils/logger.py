import logging
import os

os.makedirs("logs", exist_ok=True)

logger = logging.getLogger("bank_logger")
logger.setLevel(logging.DEBUG)

# Formatter
formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')


file_handler = logging.FileHandler("logs/errors.log")
file_handler.setLevel(logging.WARNING) 
file_handler.setFormatter(formatter)

console_handler = logging.StreamHandler()
console_handler.setLevel(logging.INFO)  
console_handler.setFormatter(formatter)

# Add handlers to the logger
logger.addHandler(file_handler)
logger.addHandler(console_handler)
