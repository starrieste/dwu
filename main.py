from dwu.utils import log_crash
from dwu.systray import TrayIcon

def main():
    try:
        tray_icon = TrayIcon()
        tray_icon.run()
    except Exception as e:
        log_crash(e)

if __name__ == "__main__":
    main()