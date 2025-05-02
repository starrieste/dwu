import os
import sys
import time
import datetime
from dwu.logger import logger

def log_crash(e):
    exc_type, exc_value, exc_traceback = sys.exc_info()
    crash_str = f"Unhandled exception: {exc_type.__name__} - {str(e)}"
    logger.error(crash_str)
    with open(f"logs/crash/{int(time.time())}.txt", "w") as crash_file:
        crash_file.write(crash_str)
