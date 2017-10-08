#!/usr/bin/env python
# -*- coding: utf-8 -*-

from answers import prompts
from answers import document
import click

@click.group()
def cli():
    pass

@cli.command()
def free():
    click.echo(document.prompt('enter text:'))

@cli.command()
def choice():
    click.echo(prompts.choice('Choose an option', ['option 1', 'option 2', 'option 3']))

@cli.command()
def single():
    click.echo(prompts.choice('Pick a number', [1234, 4238, 43230, 209348], multi=False))

if __name__ == "__main__":
    cli()
