from .utils import log_crash
from .cli import run_cli
from .gui import run_gui

if __name__ == '__main__':
    try:
        # run_cli()
        run_gui()
    except Exception as e:
        log_crash(e)