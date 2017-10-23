#!/usr/bin/env python
# -*- coding: utf-8 -*-

from answers import choose
from answers import document
from answers import yesno
import click

@click.group()
def cli():
    pass

@cli.command()
def free():
    click.echo(document.prompt('enter text:'))

@cli.command()
def choice():
    click.echo(choose('Choose an option', ['option 1', 'option 2', 'option 3']))

@cli.command()
def single():
    click.echo(choose('Pick a number', [1234, 4238, 43230, 209348], multi=False))

@cli.command()
def confirm():
    click.echo(yesno.confirm('Continue with foo?: '))

if __name__ == "__main__":
    cli()
