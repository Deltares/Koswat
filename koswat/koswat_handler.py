from __future__ import annotations

import logging
from pathlib import Path
from typing import Optional

from koswat.configuration.io.koswat_run_settings_importer import (
    KoswatRunSettingsImporter,
)
from koswat.configuration.settings.koswat_run_settings import KoswatRunScenarioSettings
from koswat.cost_report.io.csv.summary_matrix_csv_exporter import (
    SummaryMatrixCsvExporter,
)
from koswat.cost_report.io.plots.multi_location_profile_comparison_plot_exporter import (
    MultiLocationProfileComparisonPlotExporter,
)
from koswat.cost_report.summary.koswat_summary import KoswatSummary
from koswat.cost_report.summary.koswat_summary_builder import KoswatSummaryBuilder
from koswat.koswat_logger import KoswatLogger


class KoswatHandler:
    def _generate_summary(
        self, run_scenario: KoswatRunScenarioSettings
    ) -> KoswatSummary:
        _summary_builder = KoswatSummaryBuilder()
        _summary_builder.run_scenario_settings = run_scenario
        _summary = _summary_builder.build()
        logging.info("Analysis created.")
        return _summary

    def _export_summary(
        self, settings: KoswatRunScenarioSettings, summary: KoswatSummary
    ) -> None:
        # Export analysis results (csv and plots)
        settings.output_dir.mkdir(parents=True, exist_ok=True)
        logging.info("Exporting csv results to {}.".format(settings.output_dir))
        if not summary.locations_profile_report_list:
            logging.error("No summary was genarted for {}".format(settings.name))
            return
        # Export analysis csv.
        _exporter = SummaryMatrixCsvExporter()
        _exporter.data_object_model = summary
        _exporter.export_filepath = settings.output_dir / "matrix_results.csv"
        _exporter.export(_exporter.build())
        logging.info("Exported matrix results to: {}".format(_exporter.export_filepath))

    def _generate_plots(
        self, settings: KoswatRunScenarioSettings, summary: KoswatSummary
    ) -> None:
        # Export analysis plots
        for _multi_report in summary.locations_profile_report_list:
            try:
                _mlp_plot = MultiLocationProfileComparisonPlotExporter()
                _mlp_plot.cost_report = _multi_report
                _mlp_plot.export_dir = settings.output_dir
                _mlp_plot.export()
                logging.info(
                    "Exported comparison plots to: {}".format(settings.output_dir)
                )
            except Exception as e_info:
                logging.error(
                    "Failed to export report comparison plots for {}.".format(
                        _multi_report.profile_type
                    )
                )
                logging.error(e_info)

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
        for _run_scenario in self._run_settings.run_scenarios:
            try:
                _summary = self._generate_summary(_run_scenario)
                self._export_summary(_run_scenario, _summary)
                self._generate_plots(_run_scenario, _summary)
            except Exception as e_info:
                logging.error(
                    "Error while running scenario {}, more details: {}".format(
                        _run_scenario.name, e_info
                    )
                )
                if __debug__:
                    raise

    def __enter__(self) -> KoswatHandler:
        self._logger = KoswatLogger.init_logger(Path("koswat.log"))
        logging.info("Initialized Koswat.")
        return self

    def __exit__(self, *args, **kwargs) -> None:
        logging.info("Finalized Koswat.")
