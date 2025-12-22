import click
from .splash import splash
from .manager import WallpaperManager
from .metadata import WallpaperMetadata

def print_version(ctx, param, value):
    if not value or ctx.resilient_parsing:
        return
    click.echo("DWU (Daily Wallpaper Updater) 0.1.3")
    ctx.exit()

@click.command()
@click.option('--version', is_flag=True, expose_value=False, callback=print_version, is_eager=True, help="Output current version")
@click.option('--daily', is_flag=True, help="Set today\'s Wallpaper")
@click.option('--credits', is_flag=True, help="Display the artist and source of the current wallpaper")
def main(daily: bool, credits: bool):
    show_splash: bool = True
    
    if credits:
        metadata = WallpaperMetadata.load_current()
        if not metadata:
            click.echo("No wallpaper metadata found")
            return
        
        click.echo("Credits:")
        if metadata.artist:
            click.echo(f"    Artist: {metadata.artist}")
        if metadata.artist:
            click.echo(f"    Source: {metadata.source}")
        show_splash = False
    
    if daily:
        wallman = WallpaperManager()
        wallman.update_wallpaper()
        click.echo("Wallpaper updated!")
        show_splash = False

    if show_splash:
        click.echo(splash)

if __name__ == '__main__':
    main()
