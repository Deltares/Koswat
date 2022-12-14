from __future__ import annotations

import logging
from pathlib import Path
from typing import Optional

from koswat.configuration.io.koswat_run_settings_importer import (
    KoswatRunSettingsImporter,
)
from koswat.cost_report.io.csv.summary_matrix_csv_exporter import (
    SummaryMatrixCsvExporter,
)
from koswat.cost_report.io.plots.multi_location_profile_comparison_plot_exporter import (
    MultiLocationProfileComparisonPlotExporter,
)
from koswat.cost_report.summary.koswat_summary_builder import KoswatSummaryBuilder
from koswat.dike.surroundings.wrapper.surroundings_wrapper_builder import (
    SurroundingsWrapperBuilder,
)
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
        _config_importer = KoswatRunSettingsImporter()
        _config_importer.ini_configuration = _as_path(analysis_file)
        self._koswat_config = _config_importer.build()

        # Generate an output dir.
        self._koswat_config.output_dir.mkdir(exist_ok=True, parents=True)

        # Run data
        for _input_profile in self._koswat_config.input_profiles:
            _profile_output_dir = (
                self._koswat_config.output_dir / _input_profile.input_data.dike_section
            )
            _profile_output_dir.mkdir(exist_ok=True, parents=True)

            for _scenario in self._koswat_config.scenarios:
                _multi_loc_multi_prof_cost_builder = KoswatSummaryBuilder()
                # _multi_loc_multi_prof_cost_builder.surroundings = _surroundings
                # _surroundings = SurroundingsWrapperBuilder.from_files(
                #     dict(csv_file=_csv_surroundings_file, shp_file=_shp_trajects_file)
                # ).build()
                _multi_loc_multi_prof_cost_builder.base_profile = _input_profile
                _multi_loc_multi_prof_cost_builder.scenario = _scenario
                _summary = _multi_loc_multi_prof_cost_builder.build()

                _exporter = SummaryMatrixCsvExporter()
                _exporter.data_object_model = _summary
                _exporter.export_filepath = _profile_output_dir / "matrix_results.csv"
                _exporter.export(_exporter.build())

                for _multi_report in _summary.locations_profile_report_list:
                    _mlp_plot = MultiLocationProfileComparisonPlotExporter()
                    _mlp_plot.cost_report = _multi_report
                    _mlp_plot.export_dir = _profile_output_dir
                    _mlp_plot.export()

    def __enter__(self) -> KoswatHandler:
        self._logger = KoswatLogger.init_logger(Path("koswat.log"))
        return self

    def __exit__(self, *args, **kwargs) -> None:
        try:
            _analysis_log = self._koswat_config.output_dir / _analysis_log
            self._logger.log_file.rename(_analysis_log)
        except Exception as e_err:
            logging.error("Log file could not be moved.")
