from __future__ import annotations

import math

import pytest

from koswat.calculations.list_multi_location_profile_cost_builder import (
    ListMultiProfileCostBuilder,
)
from koswat.calculations.profile_cost_builder import ProfileCostBuilder
from koswat.calculations.profile_reinforcement import ProfileReinforcementCalculation
from koswat.koswat_report import (
    LayerCostReport,
    MultiLocationProfileCostReport,
    ProfileCostReport,
)
from koswat.koswat_scenario import KoswatScenario
from koswat.profiles.koswat_profile import KoswatProfileBase
from koswat.profiles.koswat_profile_builder import KoswatProfileBuilder
from koswat.surroundings.koswat_buildings_polderside import KoswatBuildingsPolderside
from koswat.surroundings.koswat_surroundings import KoswatSurroundings
from koswat.surroundings.koswat_surroundings_builder import KoswatSurroundingsBuilder
from tests import test_data
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

    acceptance_test_cases = [
        pytest.param(
            dict(
                layers=LayersCases.without_layers,
                input_profile=InputProfileCases.default,
                scenario=ScenarioCases.default,
            ),
            id="Default Reinforcement without layers.",
        ),
        pytest.param(
            dict(
                layers=LayersCases.with_clay,
                input_profile=InputProfileCases.default,
                scenario=ScenarioCases.default,
            ),
            id="Default Reinforcement with layers.",
        ),
    ]

    @pytest.mark.parametrize("input_profile_case", InputProfileCases.cases)
    @pytest.mark.parametrize("scenario_case", ScenarioCases.cases)
    @pytest.mark.parametrize(
        "layers_case",
        LayersCases.cases,
    )
    def test_given_surrounding_files_run_calculations_for_all_included_profiles(
        self, input_profile_case, scenario_case, layers_case
    ):
        # 1. Define test data.
        _csv_test_file = (
            test_data / "csv_reader" / "Omgeving" / "T_10_3_bebouwing_binnendijks.csv"
        )
        _shp_test_file = (
            test_data
            / "shp_reader"
            / "Dijkvak"
            / "Dijkringlijnen_KOSWAT_Totaal_2017_10_3_Dijkvak.shp"
        )
        assert _csv_test_file.is_file()
        assert _shp_test_file.is_file()

        _surroundings = KoswatSurroundingsBuilder.from_files(
            dict(csv_file=_csv_test_file, shp_file=_shp_test_file)
        ).build()
        assert isinstance(_surroundings, KoswatSurroundings)
        assert isinstance(_surroundings.buldings_polderside, KoswatBuildingsPolderside)

        _scenario = KoswatScenario.from_dict(scenario_case)
        assert isinstance(_scenario, KoswatScenario)

        _base_profile = KoswatProfileBuilder.with_data(
            dict(
                input_profile_data=input_profile_case,
                layers_data=layers_case,
            )
        ).build(KoswatProfileBase)

        # 2. Run test
        _list_multi_profile_cost_builder = ListMultiProfileCostBuilder()
        _list_multi_profile_cost_builder.surroundings = _surroundings
        _list_multi_profile_cost_builder.base_profile = _base_profile
        _list_multi_profile_cost_builder.scenario = _scenario
        _multi_report_list = _list_multi_profile_cost_builder.build()

        # 3. Verify expectations.
        assert any(_multi_report_list)
        for _multi_report in _multi_report_list:
            assert isinstance(_multi_report, MultiLocationProfileCostReport)
            assert isinstance(_multi_report.profile_cost_report, ProfileCostReport)
            assert _multi_report.total_cost > 0
            assert _multi_report.total_volume > 0
            _layers_report = _multi_report.profile_cost_report.layer_cost_reports
            assert len(_layers_report) == 1 + len(layers_case["coating_layers"])
            assert all(isinstance(lcr, LayerCostReport) for lcr in _layers_report)
