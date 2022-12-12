import logging
from pathlib import Path
from typing import Optional

import click

from koswat.configuration.io.koswat_configuration_importer import (
    KoswatConfigurationImporter,
)


### Below is the documentation for the commandline interface, see the CLICK-package.
@click.command()
@click.option("--input_file", default=None, help="Full path to the ini input file.")
def run_analysis(input_file: str):
    def _as_path(ini_file: str) -> Optional[Path]:
        _ini = Path(ini_file)
        if not _ini.is_file():
            raise FileNotFoundError(_ini)
        return _ini

    _config_importer = KoswatConfigurationImporter()
    _config_importer.ini_configuration = _as_path(input_file)
    _koswat_config = _config_importer.build()
    _koswat_config.run()


if __name__ == "__main__":
    try:
        run_analysis()
    except Exception as e_info:
        logging.error(str(e_info))
