import click
import sys

from .splash import splash
from .wallpaper_manager import WallpaperManager, WallpaperSetError
from .metadata import WallpaperMetadata
from .skip_manager import SkipManager
from .scraper import WallpaperScraper
from .utils import print_wall_feedback

def print_version(ctx, param, value):
    if not value or ctx.resilient_parsing:
        return
    click.echo("DWU (Daily Wallpaper Updater) 1.0.1")
    ctx.exit()

@click.command()
@click.option('--version', is_flag=True, expose_value=False, callback=print_version, is_eager=True, help="Output current version")

@click.option('--status', is_flag=True, help="Display info about the current status")

@click.option('--today', is_flag=True, help="Set today's wallpaper or the most recent unskipped wallpaper")
@click.option('--back', type=click.INT, help="Set to wallpaper from an amount of days back. Ignores skips.")

@click.option('--skip', is_flag=True, help="Skip this wallpaper. DWU will try to find the most recent non-skipped wallpaper to set instead if you run --today.")
@click.option('--unskip', type=click.INT, help="Unskip a wallpaper. 0 is today, then 1-9 is days before today.")
@click.option('--unskip-all', is_flag=True, help="Unskip all wallpapers.")
@click.option('--list-skipped', is_flag=True, help="List currently skipped wallpapers")

@click.option('--show-metadata', is_flag=True, help="Display metadata of the current wallpaper")
@click.option('--credits', is_flag=True, help="Display the artist and source of the current wallpaper. Removes watermark if run")

def main(
    status: bool,
    today: bool,
    credits: bool,
    back: int | None,
    skip: bool,
    unskip: int | None,
    unskip_all: bool,
    list_skipped: bool,
    show_metadata: bool
):
    try:
        wallman = WallpaperManager()
    except Exception as e:
        click.secho(f"Error: {e}", fg="red")
        sys.exit(1)
    
    if status:
        try:
            click.echo(wallman._backend.name)
        except Exception as e:
            click.secho(f"Error: {e}", fg="red")
            sys.exit(1)
        
    elif today:
        try:
            print_wall_feedback(wallman.update_auto())
        except WallpaperSetError as e:
            click.secho(f"Error: {e}", fg="red")
            sys.exit(1)
    
    elif back is not None:
        try:
            print_wall_feedback(wallman.update_back(back))
        except WallpaperSetError as e:
            click.secho(f"Error: {e}", fg="red")
            sys.exit(1)
        except RuntimeError as e:
            click.secho(f"Error: {e}", fg="red")
            sys.exit(1)
        
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
    
    elif show_metadata:
        meta = WallpaperMetadata.load()
        click.echo(meta)
        
    else:
        click.echo(splash)
