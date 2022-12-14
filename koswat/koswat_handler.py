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
        _run_settings_importer = KoswatRunSettingsImporter()
        _run_settings_importer.ini_configuration = _as_path(analysis_file)
        self._run_settings = _run_settings_importer.build()

        # Run data
        for _input_profile in self._run_settings.input_profile_cases:
            _profile_output_dir = (
                self._run_settings.output_dir / _input_profile.input_data.dike_section
            )
            _profile_output_dir.mkdir(exist_ok=True, parents=True)

            for _run_scenario in self._run_settings.run_scenarios:
                # Generate Analysis
                _summary_builder = KoswatSummaryBuilder()
                _summary_builder.base_profile = _input_profile
                _summary_builder.scenario = _run_scenario.scenario
                _summary_builder.surroundings = _run_scenario.surroundings
                logging.info(
                    "Creating analysis for {} - scenario {} - {}".format(
                        _input_profile.input_data.dike_section,
                        _run_scenario.scenario.scenario_section,
                        _run_scenario.scenario.scenario_name,
                    )
                )
                _summary = _summary_builder.build()
                logging.info("Analysis created.")
                # Export analysis results (csv and plots)
                _run_scenario_output = _profile_output_dir / _run_scenario.output_dir
                _run_scenario_output.mkdir(parents=True, exist_ok=True)
                logging.info(
                    "Exporting csv results to {}.".format(_run_scenario_output)
                )
                # Export analysis csv.
                _exporter = SummaryMatrixCsvExporter()
                _exporter.data_object_model = _summary
                _exporter.export_filepath = _run_scenario_output / "matrix_results.csv"
                _exporter.export(_exporter.build())
                logging.info(
                    "Exported matrix results to: {}".format(_exporter.export_filepath)
                )
                # Export analysis plots
                for _multi_report in _summary.locations_profile_report_list:
                    _mlp_plot = MultiLocationProfileComparisonPlotExporter()
                    _mlp_plot.cost_report = _multi_report
                    _mlp_plot.export_dir = _run_scenario_output
                    _mlp_plot.export()
                    logging.info(
                        "Exported comparison plots to: {}".format(_run_scenario_output)
                    )

    def __enter__(self) -> KoswatHandler:
        self._logger = KoswatLogger.init_logger(Path("koswat.log"))
        return self

    def __exit__(self, *args, **kwargs) -> None:
        try:
            _analysis_log = self._run_settings.output_dir / _analysis_log
            self._logger.log_file.rename(_analysis_log)
        except Exception as e_err:
            logging.error("Log file could not be moved.")
