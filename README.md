# DWU - Daily Wallpaper Updater

DWU is a CLI tool that updates your desktop wallpaper each day to the latest anime wallpaper from [wallpaper-a-day.com](https://wallpaper-a-day.com)  
If you run into any issues, please feel free to make an issue on this repository.  

## Installation

### Arch Linux (AUR)

```bash
yay -S dwu
```

### Other Distros (PyPI Package)

```bash
pipx install dwu
```

### Wallpaper Setting

You do need to manually install a capable wallpaper setter.  
Right now, the only supported ones are awww, swww, feh, and nitrogen  
  
If you want to use a different one, make an [issue](https://github.com/starrieste/dwu/issues) or [PR](https://github.com/starrieste/dwu/pulls)  
If you use swww, consider switching to awww, as swww is now archived. The author's explanation is [here](https://www.lgfae.com/posts/2025-10-29-RenamingSwww.html)

## Usage

Set to today's wallpaper

```bash
dwu --today
```

Set to the wallpaper from a certain amount of days before today (there's a limit of 9 right now for this, might fix later)

```bash
dwu --back 2 # 2 days before today's wallpaper
```

The wallpaper has a watermark to credit the artist in the bottom right corner.  
Without artists, you wouldn't get amazing wallpapers! So please do show them some support!  
To remove it (for the current wallpaper instance only), run the following command.  

```bash
dwu --credits
```

For automatic hourly updates, use systemd if you're on Arch. If not, you might need to figure something out yourself.

```bash
systemctl --user enable --now dwu.timer
```

## Contribution

You can make issues and PRs, that would be awesome
