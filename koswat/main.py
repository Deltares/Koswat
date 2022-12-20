import logging

import click

from koswat.koswat_handler import KoswatHandler


### Below is the documentation for the commandline interface, see the CLICK-package.
@click.command()
@click.option("--input_file", default=None, help="Full path to the ini input file.")
def run_analysis(input_file: str):
    with KoswatHandler() as _handler:
        _handler.run_analysis(input_file)


if __name__ == "__main__":
    try:
        run_analysis()
    except Exception as e_info:
        logging.error(str(e_info))
