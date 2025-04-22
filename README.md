# DWU - Daily Wallpaper Updater

DWU (pronounced dee-woo) is a Python application that updates your Windows 11 desktop background daily to a new anime wallpaper courtesy of [wallpaper-a-day.com](https://wallpaper-a-day.com).  
It can run on startup and stays out of your way in the system tray :3

## Features
- A GUI control panel made using PyQt6
- Minimizing to system tray
- Automatic wallpaper updates as long as it's running
- Run automatically on startup!

## Compiling Source Code
1. Install python
2. Clone the repository
3. Install the required modules
```
pip -r requirements.txt
```
4. Compile using pyinstaller
```
pyinstaller --distpath . main.spec
```

## Installation Using Binaries
1. Download the desired version
2. Extract the zip file's contents to its own folder
3. Run dwu.exe

## Usage
- After running the executable, the program will be an icon in your system tray.  
- Right click it to open the GUI and for more options.  
- The program will update the wallpaper every 10 minutes, if the "check loop" is turned on.  
- You can turn on "Run at startup" to make the program start with your computer.  