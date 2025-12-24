import click

from .splash import splash
from .manager import WallpaperManager
from .metadata import WallpaperMetadata

@click.command()
@click.version_option(package_name="dwu")
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
            
        wallman = WallpaperManager()
        if metadata.add_watermark:
            wallman.unwatermark(metadata)
            
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
