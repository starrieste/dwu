import click
from .splash import splash

@click.command()
@click.option('--version', is_flag=True, help='Output current version')
@click.option('--daily', is_flag=True, help='Set your wallpaper to today\'s wallpaper')

def cli(version: bool = False, daily: bool = False):
    show_splash: bool = True
    if version:
        click.echo("DWU (Daily Wallpaper Updater) 0.1.0")
        show_splash = False
    if daily:
        # TODO: update wallpaper here
        click.echo("Wallpaper updated!")
        show_splash = False

    if show_splash:
        click.echo(splash)

if __name__ == '__main__':
    cli()
