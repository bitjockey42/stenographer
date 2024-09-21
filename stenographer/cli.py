import click

from stenographer.bot import start_bot


@click.group()
def cli():
    pass


@cli.command()
def start():
    """Start the bot"""
    start_bot()
