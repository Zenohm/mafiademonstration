#!/usr/bin/env python2
# -*- coding: utf-8 -*-

import os
os.environ["KIVY_NO_ARGS"] = "1"

import click

from mafiademonstration.mafiademonstration import MafiaDemonstrationApp


@click.command()
@click.option(
    '-l', '--language', help='Default language of the App', default='en',
    type=click.Choice(['en', 'es', 'de', 'fr'])
)
def main(language):
    """Run MafiaDemonstrationApp with the given language setting.
    """
    MafiaDemonstrationApp(language).run()
