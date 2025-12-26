<img width="1289" height="735" alt="dwu" src="https://github.com/user-attachments/assets/811da782-793d-44cb-b844-e16626077e00" />


<h4 align=center>DWU (Daily Wallpaper Updater) is a CLI tool that updates your desktop wallpaper each day to the latest anime wallpaper from <a href=https://wallpaper-a-day.com>wallpaper-a-day.com</a>  </h4>

## Installation

### Arch Linux (AUR)

```bash
yay -S dwu
```

### Other Distros (PyPI Package)

```bash
pipx install dwu
```

### Wallpaper Backend

You need to manually install a capable wallpaper backend.  
Right now, the supported ones are `awww`, `swww`, `feh`, and `nitrogen`  

If you use swww, consider switching to awww, as swww is now archived. The author's explanation is [here](https://www.lgfae.com/posts/2025-10-29-RenamingSwww.html)

## Usage

Set to today's wallpaper

```bash
dwu --today
```

If you don't like a certain day's wallpaper, you can skip it:
```bash
dwu --skip
```

Set to the wallpaper from a certain amount of days before today (integer should be from 0-9)

```bash
dwu --back 2 # 2 days before today's wallpaper
```

For automatic hourly updates, use systemd if you're on Arch. If not, you might need to figure something out yourself.

```bash
systemctl --user enable --now dwu.timer
```

The wallpaper has a watermark to credit the artist in the bottom right corner.  
Without artists, you wouldn't get amazing wallpapers! So please do show them some support!  
To remove it (for the current wallpaper), run the following command.  

```bash
dwu --credits
```
