from __future__ import annotations

import logging
from pathlib import Path
from typing import Optional

from koswat.configuration.io.koswat_settings_importer import KoswatConfigurationImporter
from koswat.configuration.koswat_run_configuration import KoswatRunConfiguration
from koswat.configuration.settings.koswat_general_settings import KoswatGeneralSettings
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
        _config_importer = KoswatConfigurationImporter()
        _config_importer.ini_configuration = _as_path(analysis_file)
        self._koswat_config = _config_importer.build()

        # Generate scenarios
        _run_configuration = KoswatRunConfiguration.from_settings(self._koswat_config)
        self._koswat_settings.analysis_settings.analysis_output.mkdir(
            parents=True, exist_ok=True
        )

        # Run analysis.
        _run_configuration.run()

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
