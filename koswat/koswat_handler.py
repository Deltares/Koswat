from __future__ import annotations

import logging
from pathlib import Path
from typing import Optional

from koswat.configuration.io.koswat_settings_importer import KoswatSettingsFomImporter
from koswat.koswat_logger import KoswatLogger


class KoswatHandler:
    def run_analysis(self, analysis_file: str) -> None:
        def _as_path(ini_file: str) -> Optional[Path]:
            _ini = Path(ini_file)
            if not _ini.is_file():
                logging.error("File not found at {}".format(analysis_file))
                raise FileNotFoundError(_ini)
            return _ini

        # Import data.
        _config_importer = KoswatSettingsFomImporter()
        _config_importer.ini_configuration = _as_path(analysis_file)
        self._koswat_config = _config_importer.build()

        # Generate scenarios

    def __enter__(self) -> KoswatHandler:
        self._logger = KoswatLogger.init_logger(Path("koswat.log"))
        return self

    def __exit__(self, *args, **kwargs) -> None:
        try:
            _output_dir = self._koswat_config.analysis_settings.analysis_output
            _analysis_log = _output_dir / _analysis_log
            self._logger.log_file.rename(_analysis_log)
        except Exception as e_err:
            logging.error("Log file could not be moved.")
