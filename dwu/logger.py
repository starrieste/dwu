import logging
import os
import time

# Create logs directory
os.makedirs("logs", exist_ok=True)

# Log file for the current session
log_filename = f"logs/{int(time.time())}.log"

# Configure the logger
logging.basicConfig(
    level=logging.DEBUG,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    handlers=[
        logging.FileHandler(log_filename),
        logging.StreamHandler()  # Optional: Print logs to the console
    ]
)

# Get the logger instance
logger = logging.getLogger(__name__)