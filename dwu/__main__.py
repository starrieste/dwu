import click

from .splash import splash
from .manager import WallpaperManager
from .metadata import WallpaperMetadata

def print_version(ctx, param, value):
    if not value or ctx.resilient_parsing:
        return
    click.echo("DWU (Daily Wallpaper Updater) 0.3.2")
    ctx.exit()

@click.command()
@click.option('--version', is_flag=True, expose_value=False, callback=print_version, is_eager=True, help="Output current version")
@click.option('--credits', is_flag=True, help="Display the artist and source of the current wallpaper. Removes watermark if run")
@click.option('--today', is_flag=True, help="Set today\'s Wallpaper")
@click.option('--back', type=click.INT, help="Set to wallpaper from an amount of days back")

def main(today: bool, credits: bool, back: int):
    show_splash: bool = True
    
    if credits:
        metadata = WallpaperMetadata.load_current()
        if not metadata:
            click.echo("No wallpaper metadata found")
            return
        
        click.echo(f"Day {metadata.day} Credits:")
        if metadata.artist:
            click.echo(f"    Artist: {metadata.artist}")
        if metadata.artist:
            click.echo(f"    Source: {metadata.source}")
            
        if metadata.add_watermark:
            wallman = WallpaperManager()
            wallman.unwatermark(metadata)
            click.echo("\nWatermark removed! Please show the artist some love!")
            
        show_splash = False
    
    if today:
        wallman = WallpaperManager()
        status = wallman.update_wallpaper()
        if status:
            click.echo("Wallpaper updated!")
        else:
            click.echo("Wallpaper unchanged")
        show_splash = False
        
    elif back is not None:
        wallman = WallpaperManager()
        status = wallman.update_wallpaper(back)
        if status:
            click.echo("Wallpaper updated!")
        else:
            click.echo("Wallpaper unchanged")
        show_splash = False

    if show_splash:
        click.echo(splash)

if __name__ == '__main__':
    main()
