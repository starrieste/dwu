import click
from .splash import splash
from .wallpaper_manager import WallpaperManager

def print_version(ctx, param, value):
    if not value or ctx.resilient_parsing:
        return
    click.echo("DWU (Daily Wallpaper Updater) 0.1.0")
    ctx.exit()

@click.command()
@click.option('--version', is_flag=True, expose_value=False, callback=print_version, is_eager=True, help="Output current version")
@click.option('--daily', is_flag=True, help="Set today\'s Wallpaper")

def cli(daily: bool):
    wallman = WallpaperManager()
    show_splash: bool = True
    
    if daily:
        wallman.update_wallpaper()
        click.echo("Wallpaper updated!")
        show_splash = False

    if show_splash:
        click.echo(splash)

if __name__ == '__main__':
    cli()
