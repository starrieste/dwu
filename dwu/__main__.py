from .cli import run_terminal
from .utils import log_crash

if __name__ == '__main__':
    try:
        run_terminal()
    except Exception as e:
        log_crash(e)