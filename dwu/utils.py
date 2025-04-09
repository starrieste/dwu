import os
import sys
import time
import logging

def log_crash(e):
    exc_type, exc_value, exc_traceback = sys.exc_info()
    if exc_traceback:
        crash_str = f"Error on line {exc_traceback.tb_lineno}: {str(e)}"
    else:
        crash_str = f"Error: {str(e)}"

    logging.error(crash_str)
    timeX = str(time.time())
    os.makedirs("crashlogs", exist_ok=True)
    with open(f"crashlogs/CRASH-{timeX}.txt", "w") as logfile:
        logfile.write(crash_str)
