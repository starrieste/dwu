import logging
import os
from datetime import datetime

# Create logs directory
os.makedirs("logs", exist_ok=True)

# Log file for the current session
log_filename = f"logs/session_{datetime.now().strftime('%Y-%m-%d_%H-%M-%S')}.log"

# Configure the logger
logging.basicConfig(
    level=logging.DEBUG,
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[
        logging.FileHandler(log_filename),
        logging.StreamHandler()  # Optional: Print logs to the console
    ]
)

# Get the logger instance
logger = logging.getLogger(__name__)