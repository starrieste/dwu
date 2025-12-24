# DWU - Daily Wallpaper Updater

DWU is a CLI tool that updates your desktop wallpaper daily to the latest anime wallpaper from [wallpaper-a-day.com](https://wallpaper-a-day.com)  


## Installation

### Arch Linux (AUR)

```bash
yay -S dwu
```

### Pip

```bash
pipx install dwu
```

## Usage

Set to today's wallpaper

```bash
dwu --today
```

For automatic hourly updates, use systemctl

```bash
systemctl --user enable --now dwu.timer
```
