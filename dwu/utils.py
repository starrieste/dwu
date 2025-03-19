import os
import sys
import time

def log_crash(e):
    crash = [
        f"Error on line {sys.exc_info()[-1].tb_lineno}",
        "\n",
        str(e)
    ]
    crash_str = ''.join(crash)
    print(crash_str)
    timeX = str(time.time())
    os.makedirs("crashlogs", exist_ok=True)
    with open(f"crashlogs/CRASH-{timeX}.txt", "w") as logfile:
        logfile.write(crash_str)
