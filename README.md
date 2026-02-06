<p align=center>
  <img width="800" alt="dwu" src="https://github.com/user-attachments/assets/811da782-793d-44cb-b844-e16626077e00">
</p>

<p align="center">
  <a href="https://aur.archlinux.org/packages/dwu">
    <img src="https://img.shields.io/aur/version/dwu?style=flat-square" alt="AUR">
  </a>
  <a href="https://pypi.org/project/dwu/">
    <img src="https://img.shields.io/pypi/v/dwu?style=flat-square" alt="PyPI">
  </a>
  <a href="https://github.com/starrieste/dwu/stargazers">
    <img src="https://img.shields.io/github/stars/starrieste/dwu?style=flat-square" alt="Stars">
  </a>
</p>

---
<p align=center>A CLI tool that updates your desktop wallpaper each day to the latest anime wallpaper from<br><a href=https://wallpaper-a-day.com>wallpaper-a-day.com</a>  </p>

<h1>Installation</h1>

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

<h1>Usage</h1>

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

If you like a wallpaper, you can save it!

```bash
dwu --save-dir ~/Wallpapers
dwu --save
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

h1>Thank You!</h1>

If you like this project, please share it with your friends!
I'm just starting out, and it would mean the world to me :D
