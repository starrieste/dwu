import os
import random
import click
import sys

from dwu.config_manager import Config
from dwu.splash import splash
from dwu.wallpaper_manager import WallpaperManager
from dwu.metadata import WallpaperMetadata
from dwu.skip_manager import SkipManager
from dwu.scraper import WallpaperScraper
from dwu.utils import print_wall_feedback

def print_version(ctx, param, value):
    if not value or ctx.resilient_parsing:
        return
    click.echo("DWU (Daily Wallpaper Updater) 1.2.0")
    ctx.exit()

@click.command()
@click.option('--version', is_flag=True, expose_value=False, callback=print_version, is_eager=True, help="Output current version")

@click.option('--status', is_flag=True, help="Display info about the current status")

@click.option('--today', is_flag=True, help="Set today's wallpaper or the most recent unskipped wallpaper")
@click.option('--back', type=click.INT, help="Set to wallpaper from an amount of days back. Ignores skips.")
@click.option('--save', is_flag=True, help="Save the current wallpaper")
@click.option('--save-dir', type=click.STRING, help="Set the save directory where you want to save the wallpapers.")

@click.option('--skip', is_flag=True, help="Skip this wallpaper. DWU will try to find the most recent non-skipped wallpaper to set instead if you run --today.")
@click.option('--unskip', type=click.INT, help="Unskip a wallpaper. 0 is today, then 1-9 is days before today.")
@click.option('--unskip-all', is_flag=True, help="Unskip all wallpapers.")
@click.option('--list-skipped', is_flag=True, help="List currently skipped wallpapers")

@click.option('--credits', is_flag=True, help="Display the artist and source of the current wallpaper. Removes watermark if run")

def main(
    status: bool,
    today: bool,
    back: int | None,
    save: bool,
    save_dir: str | None,
    skip: bool,
    unskip: int | None,
    unskip_all: bool,
    list_skipped: bool,
    credits: bool,
):
    try:
        wallman = WallpaperManager()
        
        if status:
            click.echo("Backend: " + wallman.get_backend_name())
            meta = WallpaperMetadata.load()
            click.echo("Currently Set: " + ("yes" if wallman.currently_set(meta) else "no"))
            click.echo(meta)
            
        elif today:
            print_wall_feedback(wallman.update_auto())
        
        elif back is not None:
            print_wall_feedback(wallman.update_back(back))
        
        elif save:
            save_folder = Config().get("save_dir") or os.path.join(os.path.expanduser("~"), "dwu_saved_wallpapers")
            os.makedirs(save_folder, exist_ok=True)
            meta = WallpaperMetadata.load()
            if meta is None:
                click.echo("No currently set wallpaper")
            else:
                save_path = os.path.join(save_folder, "dwu-" + str(meta.day) +"-" + str(meta.get_img_name()))
                wallman.download_image(meta, save_path)
                click.echo(f"Successfully saved wallpaper to {save_path}")
        
        elif save_dir is not None:
            path = os.path.expanduser(save_dir)
            path = os.path.abspath(path)
            Config().set("save_dir", path)
            click.echo(f"Changed save directory to {path}")
                    
        elif skip:
            meta = WallpaperMetadata.load()
            skips = SkipManager()
        
            if not meta or not meta.successfully_set:
                click.echo("No active wallpaper to skip.")
                return
        
            skips.add(meta.img_url)
            print_wall_feedback(wallman.update_auto())
            
        elif unskip is not None:
            wall = WallpaperScraper().get_all()[unskip]
            SkipManager().unskip(wall.img_url)
        
        elif unskip_all:
            SkipManager().unskip_all()
            
        elif list_skipped:
            skips = SkipManager()
            walls = WallpaperScraper().get_all()
            skipped = []
            for i, meta in enumerate(walls):
                if skips.is_skipped(meta.img_url):
                    skipped.append(i)
            click.echo(skipped if len(skipped) > 0 else "No skipped wallpapers.")
            
        elif credits:
            meta = WallpaperMetadata.load()
            if not meta:
                click.echo("No wallpaper metadata found")
                return
        
            click.echo(f"Day {meta.day} Credits:")
            if meta.artist:
                click.echo(f"    Artist: {meta.artist}")
            if meta.source:
                click.echo(f"    Source: {meta.source}")
        
            if meta.add_watermark:
                wallman.unwatermark(meta)
            
        else:
            click.secho(
                splash,
                fg=random.choice((
                    "black",
                    "red",
                    "green",
                    "yellow",
                    "blue",
                    "magenta",
                    "cyan",
                    "white",
                    "bright_black",
                    "bright_red",
                    "bright_green",
                    "bright_yellow",
                    "bright_blue",
                    "bright_magenta",
                    "bright_cyan",
                    "bright_white",
                ))
            )
            
    except Exception as e:
        click.secho(f"Error: {e}", fg="red")
        sys.exit(1)

if __name__ == '__main__':
    main()
