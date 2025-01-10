import pytest

from koswat.configuration.settings.koswat_scenario import KoswatScenario
from koswat.dike.koswat_input_profile_protocol import KoswatInputProfileProtocol
from koswat.dike_reinforcements.reinforcement_profile.berm_calculator.berm_calculator_result import (
    BermCalculatorResult,
)
from koswat.dike_reinforcements.reinforcement_profile.berm_calculator.keep_berm_calculator import (
    KeepBermCalculator,
)


class TestKeepBermCalculator:
    def test_calculate(
        self,
        valid_scenario: KoswatScenario,
        valid_input_profile: KoswatInputProfileProtocol,
    ):
        # 1. Define test data
        _calculator = KeepBermCalculator(
            scenario=valid_scenario,
            dikebase_piping_old=None,
            dikebase_piping_new=None,
            dike_height_new=None,
        )

        # 2. Run test
        _result = _calculator.calculate(
            base_data=valid_input_profile,
            reinforced_data=valid_input_profile,
        )

        # 3. Verify expectations
        assert isinstance(_result, BermCalculatorResult)
        assert _result.berm_width == valid_input_profile.polderside_berm_width
        assert _result.berm_height == 2.375
        assert _result.slope == pytest.approx(0.290909)

    def test__calculate_new_keep_polderside_berm_height(
        self,
        valid_scenario: KoswatScenario,
        valid_input_profile: KoswatInputProfileProtocol,
    ):
        # 1. Define test data
        _calculator = KeepBermCalculator(
            scenario=valid_scenario,
            dikebase_piping_old=None,
            dikebase_piping_new=None,
            dike_height_new=None,
        )

        # 2. Run test
        _result = _calculator._calculate_new_keep_polderside_berm_height(
            base_data=valid_input_profile,
        )

        # 3. Verify expectations
        assert isinstance(_result, float)
        assert _result == 2.375

    def test__calculate_new_keep_polderside_slope(
        self,
        valid_scenario: KoswatScenario,
        valid_input_profile: KoswatInputProfileProtocol,
    ):
        # 1. Define test data
        _calculator = KeepBermCalculator(
            scenario=valid_scenario,
            dikebase_piping_old=None,
            dikebase_piping_new=None,
            dike_height_new=None,
        )

        # 2. Run test
        _result = _calculator._calculate_new_keep_polderside_slope(
            base_data=valid_input_profile,
        )

        # 3. Verify expectations
        assert isinstance(_result, float)
        assert _result == pytest.approx(0.290909)
