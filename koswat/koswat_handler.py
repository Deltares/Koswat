from __future__ import annotations

import logging
from pathlib import Path
from typing import Optional

from koswat.configuration.io.koswat_configuration_importer import (
    KoswatConfigurationImporter,
)
from koswat.configuration.koswat_configuration import KoswatConfiguration
from koswat.dike.profile.koswat_profile import KoswatProfileBase
from koswat.dike.profile.koswat_profile_builder import KoswatProfileBuilder
from koswat.koswat_logger import KoswatLogger


class KoswatHandler:
    def _prepare_scenarios(self, koswat_config: KoswatConfiguration) -> None:
        if not koswat_config.is_valid():
            logging.error(
                "Current configuration is not valid. Analysis can't go further."
            )

        self._koswat_config.analysis_settings.analysis_output.mkdir(
            parents=True, exist_ok=True
        )

        # Define base profile:
        _input_cases = []
        for (
            _input_case
        ) in self._koswat_config.analysis_settings.dike_sections_input_profile:
            _input_profile = KoswatProfileBuilder.with_data(
                dict(
                    input_profile_data=_input_case,
                    layers_data=self._koswat_config.dike_profile_settings.get_material_thickness(),
                    profile_type=KoswatProfileBase,
                )
            )
            _input_cases.append(_input_profile)
        assert _input_cases

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
        _scenarios = self._prepare_scenarios(self._koswat_config)

        # Run analysis.
        logging.info("Running analysis")
        raise NotImplementedError()

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
