import logging
from pathlib import Path
from typing import Optional

from koswat.configuration.io.koswat_configuration_importer import (
    KoswatConfigurationImporter,
)
from koswat.koswat_logger import KoswatLogger


class KoswatHandler:
    def __init__(self) -> None:
        self._logger = KoswatLogger.init_logger("koswat.log")

    def run_analysis(self, analysis_file: str) -> None:
        def _as_path(ini_file: str) -> Optional[Path]:
            _ini = Path(ini_file)
            if not _ini.is_file():
                logging.error("File not found at {}".format(analysis_file))
                raise FileNotFoundError(_ini)
            return _ini

        _config_importer = KoswatConfigurationImporter()
        _config_importer.ini_configuration = _as_path(analysis_file)
        _koswat_config = _config_importer.build()
        _koswat_config.run()
