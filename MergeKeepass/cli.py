import getpass
import click
import pykeepass
from MergeKeepass.keepassmerge import KeepassMerger
from getpass import getpass

@click.command()
@click.option('-p', '--password', type=click.STRING)
@click.option('-d', '--debug', is_flag=True)
@click.option('-c', '--continue-on-error', is_flag=True)
@click.argument('input_databases', type=click.Path(exists=True), nargs=-1)
@click.argument('output_database', type=click.Path())
def cli(input_databases,
                output_database,
                password,
                debug,
                continue_on_error):
    print("pykeepass version : ",pykeepass.__version__)
    assert len(input_databases)

    if not password:
        password = getpass()

    merger = KeepassMerger()
    merger.merge_databases(input_databases,
                    output_database,
                    password,
                    debug,
                    continue_on_error)
