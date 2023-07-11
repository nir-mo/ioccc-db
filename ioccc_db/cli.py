import logging
import os

import click

from ioccc_winners_db import IOCCCWinnersDB, build_sqllite_db

__author__ = "Nir Moshe (nirmo)"

DEFAULT_IOCCC_WINNERS_DIRECTORY = os.path.join(os.path.dirname(__file__), "../winner")
DEFAULT_IOCCC_SQLITE_DB_PATH = os.path.join(os.path.dirname(__file__), "../ioccc_winners.sqlite")


@click.command()
@click.option(
    '--ioccc_winners_directory',
    default=DEFAULT_IOCCC_WINNERS_DIRECTORY,
    help='IOCCC winners directory, should be a clone of the following github: https://github.com/ioccc-src/winner.git.'
)
@click.option(
    '--output_file',
    default=DEFAULT_IOCCC_SQLITE_DB_PATH,
    help='Path to the output db.'
)
@click.option(
    '--force',
    is_flag=True,
    default=False,
    help='Overrides output_file if its already exists.'
)
@click.option(
    '--verbose',
    is_flag=True,
    default=False,
    help='Verbose mode.'
)
def build_db(ioccc_winners_directory, output_file, force, verbose):
    logging.basicConfig(level=logging.DEBUG if verbose else logging.INFO)
    if not os.path.exists(ioccc_winners_directory):
        logging.error(f"Can't find IOCCC winners directory {ioccc_winners_directory}")
        exit(1)

    if os.path.exists(output_file):
        if force:
            logging.debug(f"File {output_file} already exists! removing it...")
            os.remove(output_file)
        else:
            logging.error(f"File {output_file} already exists! Use --force to override it.")
            exit(1)

    logging.info(f"Building DB: {output_file}")
    winners_db = IOCCCWinnersDB(ioccc_winners_directory)
    build_sqllite_db(winners_db.get_all_entries(), output_file)
    logging.info("Done!")


if __name__ == '__main__':
    build_db()
