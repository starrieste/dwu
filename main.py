import threading
from dwu.crash_handler import log_crash
from dwu.app import *

from PyQt6.QtWidgets import QApplication
import sys

def main():
    try:
        run_app()
    except Exception as e:
        log_crash(e)

if __name__ == "__main__":
    main()