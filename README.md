# DWU - Daily Wallpaper Updater

DWU is a CLI tool written in python that updates your desktop wallpaper daily to the latest anime wallpaper from [wallpaper-a-day.com](https://wallpaper-a-day.com)  
This project currently only supports Arch-based distros wit systemd (for hourly updates) and wayland (for awww setting wallpapers)

## Installation

### Arch Linux

DWU is on the AUR!

```bash
yay -S dwu
```

## Usage

Set to today's wallpaper

```bash
dwu --daily
```

For automatic hourly updates, use systemctl

```bash
systemctl --user enable --now dwu.timer
```
