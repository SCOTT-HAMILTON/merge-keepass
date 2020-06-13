#! /usr/bin/env python3

import getpass
import click
from keepassmerge import merge_databases
from getpass import getpass

@click.command()
@click.option('-p', '--password', type=click.STRING)
@click.option('-d', '--debug', is_flag=True)
@click.argument('input_databases', type=click.Path(exists=True), nargs=-1)
@click.argument('output_database', type=click.Path())
def merge(input_databases,
                output_database,
                password,
                debug):
    assert len(input_databases)
    if not password:
        password = getpass()
    merge_databases(input_databases,
                    output_database,
                    password,
                    debug)
