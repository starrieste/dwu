from dwu.utils import log_crash
from dwu.cli import run_cli
from dwu.gui import run_gui

if __name__ == '__main__':
    try:
        # run_cli()
        run_gui()
    except Exception as e:
        log_crash(e)