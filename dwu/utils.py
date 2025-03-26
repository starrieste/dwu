import os
import sys
import time
import logging

def log_crash(e):
    crash_str = f"Error on line {sys.exc_info()[-1].tb_lineno}: {str(e)}"
    logging.error(crash_str)
    timeX = str(time.time())
    os.makedirs("crashlogs", exist_ok=True)
    with open(f"crashlogs/CRASH-{timeX}.txt", "w") as logfile:
        logfile.write(crash_str)
