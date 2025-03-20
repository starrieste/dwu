from .cli import run_terminal
from .utils import log_crash
from .gui import run_gui

if __name__ == '__main__':
    try:
        # run_terminal()
        run_gui()
    except Exception as e:
        log_crash(e)