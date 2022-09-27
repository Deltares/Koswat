# -*- coding: utf-8 -*-
import logging
from pathlib import Path
from typing import Optional

import click


### Below is the documentation for the commandline interface, see the CLICK-package.
@click.command()
@click.option("--input_file", default=None, help="Full path to the ini input file.")
def run_analysis(input_file: str):
    def _as_path(ini_file: str) -> Optional[Path]:
        if not ini_file:
            return None

        _ini = Path(ini_file)
        if not _ini.is_file():
            raise FileNotFoundError(_ini)
        return _ini

    _input_file = _as_path(input_file)


if __name__ == "__main__":
    try:
        run_analysis()
    except Exception as e_info:
        logging.error(str(e_info))
