from dwu.crash_handler import log_crash
from dwu.app import *
from dwu.logger import logger

def main():
    try:
        run_app()
    except Exception as e:
        logger.exception("Unhandled exception occurred")
        log_crash(e) # log separtely for crashes

if __name__ == "__main__":
    main()