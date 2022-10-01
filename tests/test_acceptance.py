from __future__ import annotations

import math

import pytest

from koswat.calculations.profile_reinforcement import ProfileReinforcement
from koswat.calculations.profile_reinforcement_cost_builder import (
    ProfileReinforcementCostBuilder,
)
from koswat.koswat_report import LayerCostReport, ProfileCostReport
from koswat.koswat_scenario import KoswatScenario
from koswat.profiles.koswat_profile import KoswatProfile
from koswat.profiles.koswat_profile_builder import KoswatProfileBuilder
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
        )
        pytest.param(
            dict(
                layers=LayersCases.with_clay,
                input_profile=InputProfileCases.default,
                scenario=ScenarioCases.default,
            ),
            id="Default Reinforcement with layers.",
        )
    ]

    @pytest.mark.parametrize("case_dict", acceptance_test_cases)
    def test_given_default_case_returns_costs(self, case_dict: dict):
        # 1. Define test data.
        _layers = case_dict["layers"]
        _input_profile = case_dict["input_profile"]
        _scenario = KoswatScenario.from_dict(case_dict["scenario"])
        assert isinstance(_scenario, KoswatScenario)

        _profile = KoswatProfileBuilder.with_data(_input_profile, _layers).build()
        assert isinstance(_profile, KoswatProfile)

        # 2. Run test.
        _new_profile = ProfileReinforcement().calculate_new_profile(_profile, _scenario)
        _cost_report = ProfileReinforcementCostBuilder().get_profile_cost_report(
            _profile, _new_profile
        )

        # 3. Verify expectations.
        assert isinstance(_cost_report, ProfileCostReport)
        assert isinstance(_cost_report.layer_cost_reports, list)
        assert len(_cost_report.layer_cost_reports) == 1
        assert isinstance(_cost_report.layer_cost_reports[0], LayerCostReport)
        assert not math.isnan(_cost_report.total_cost)
        assert _cost_report.total_cost > 0
        assert not math.isnan(_cost_report.total_volume)
        assert _cost_report.total_volume > 0
