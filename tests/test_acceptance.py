from __future__ import annotations

import pytest

from koswat.calculations import ReinforcementProfileBuilderFactory
from koswat.cost_report.cost_report_protocol import CostReportProtocol
from koswat.cost_report.io.csv.summary_matrix_csv_exporter import (
    SummaryMatrixCsvExporter,
)
from koswat.cost_report.io.csv.summary_matrix_csv_fom import SummaryMatrixCsvFom
from koswat.cost_report.io.plots.multi_location_profile_comparison_plot_exporter import (
    MultiLocationProfileComparisonPlotExporter,
)
from koswat.cost_report.multi_location_profile.multi_location_profile_cost_report import (
    MultiLocationProfileCostReport,
)
from koswat.cost_report.profile.profile_cost_report import ProfileCostReport
from koswat.cost_report.summary import KoswatSummary, KoswatSummaryBuilder
from koswat.dike.profile import KoswatProfileBase, KoswatProfileBuilder
from koswat.dike.surroundings.buildings_polderside.koswat_buildings_polderside import (
    KoswatBuildingsPolderside,
)
from koswat.dike.surroundings.wrapper.surroundings_wrapper import SurroundingsWrapper
from koswat.dike.surroundings.wrapper.surroundings_wrapper_builder import (
    SurroundingsWrapperBuilder,
)
from koswat.koswat_scenario import KoswatScenario
from tests import get_testcase_results_dir, test_data
from tests.library_test_cases import InputProfileCases, LayersCases, ScenarioCases


class TestAcceptance:
    def test_koswat_package_can_be_imported(self):
        """
        Import test. Not really necessary given the current way we are testing (directly to the cli). But better safe than sorry.
        """

        try:
            import koswat
            import koswat.main
        except ImportError as exc_err:
            pytest.fail(f"It was not possible to import required packages {exc_err}")

    @pytest.mark.parametrize("input_profile_case", InputProfileCases.cases)
    @pytest.mark.parametrize("scenario_case", ScenarioCases.cases)
    @pytest.mark.parametrize(
        "layers_case",
        LayersCases.cases,
    )
    def test_given_surrounding_files_run_calculations_for_all_included_profiles(
        self,
        input_profile_case,
        scenario_case,
        layers_case,
        request: pytest.FixtureRequest,
    ):
        # 1. Define test data.
        _test_dir = get_testcase_results_dir(request)
        _csv_surroundings_file = (
            test_data / "csv_reader" / "Omgeving" / "T_10_3_bebouwing_binnendijks.csv"
        )
        _shp_trajects_file = (
            test_data
            / "shp_reader"
            / "Dijkvak"
            / "Dijkringlijnen_KOSWAT_Totaal_2017_10_3_Dijkvak.shp"
        )
        assert _csv_surroundings_file.is_file()
        assert _shp_trajects_file.is_file()

        _surroundings = SurroundingsWrapperBuilder.from_files(
            dict(csv_file=_csv_surroundings_file, shp_file=_shp_trajects_file)
        ).build()
        assert isinstance(_surroundings, SurroundingsWrapper)
        assert isinstance(_surroundings.buldings_polderside, KoswatBuildingsPolderside)

        _scenario = KoswatScenario.from_dict(scenario_case)
        assert isinstance(_scenario, KoswatScenario)

        _base_koswat_profile = KoswatProfileBuilder.with_data(
            dict(
                input_profile_data=input_profile_case,
                layers_data=layers_case,
                profile_type=KoswatProfileBase,
            )
        ).build()

        # 2. Run test
        _multi_loc_multi_prof_cost_builder = KoswatSummaryBuilder()
        _multi_loc_multi_prof_cost_builder.surroundings = _surroundings
        _multi_loc_multi_prof_cost_builder.base_profile = _base_koswat_profile
        _multi_loc_multi_prof_cost_builder.scenario = _scenario
        _summary = _multi_loc_multi_prof_cost_builder.build()

        _exporter = SummaryMatrixCsvExporter()
        _exporter.data_object_model = _summary
        _exporter.export_filepath = _test_dir / "matrix_results.csv"
        _fom = _exporter.build()
        assert isinstance(_fom, SummaryMatrixCsvFom)
        _exporter.export(_fom)

        # 3. Verify expectations.
        assert isinstance(_summary, KoswatSummary)
        assert any(_summary.locations_profile_report_list)
        for (
            _reinforcement_profile
        ) in ReinforcementProfileBuilderFactory.get_available_reinforcements():
            assert any(
                isinstance(
                    _rep_profile.profile_cost_report.reinforced_profile,
                    _reinforcement_profile,
                )
                for _rep_profile in _summary.locations_profile_report_list
            ), f"Profile type {_reinforcement_profile.__name__} not found."
        for _multi_report in _summary.locations_profile_report_list:
            _mlp_plot = MultiLocationProfileComparisonPlotExporter()
            _mlp_plot.cost_report = _multi_report
            _mlp_plot.export_dir = _test_dir
            _mlp_plot.export()

        for _multi_report in _summary.locations_profile_report_list:
            assert isinstance(_multi_report, MultiLocationProfileCostReport)
            assert isinstance(_multi_report.profile_cost_report, ProfileCostReport)
            assert _multi_report.total_cost > 0
            assert _multi_report.total_volume > 0
            assert _multi_report.cost_per_km > 1000
            _layers_report = _multi_report.profile_cost_report.layer_cost_reports
            assert len(_layers_report) == (1 + len(layers_case["coating_layers"]))
            assert all(isinstance(lcr, CostReportProtocol) for lcr in _layers_report)
