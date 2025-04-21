from dwu.crash_handler import log_crash
from dwu.app import *

def main():
    try:
        run_app()
    except Exception as e:
        log_crash(e)

if __name__ == "__main__":
    main()