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
@click.argument('prompt', nargs=-1)
def free(prompt):
    prompt = prompt[0] if prompt else 'enter text: '
    click.echo(document.prompt(prompt))

@cli.command()
def choice():
    click.echo(choose('Choose an option', ['option 1', 'option 2', 'option 3']))

@cli.command()
def single():
    click.echo(choose('Pick a number', [1234, 4238, 43230, 209348], multi=False))

@cli.command()
@click.option('-q', '--quiet', is_flag=True, help='Hide the prompt and response after accepting')
@click.option('-y', '--default-true', is_flag=True, help='Expect true by default (if no choice is made)')
@click.option('-p', '--prompt', default='Continue', help='The prompt to display')
def confirm(default_true, quiet, prompt):
    """Prompt user for a yes/no response"""
    exit(not yesno.confirm(prompt, single_key=True, default=default_true, clear=quiet))

if __name__ == "__main__":
    cli()
