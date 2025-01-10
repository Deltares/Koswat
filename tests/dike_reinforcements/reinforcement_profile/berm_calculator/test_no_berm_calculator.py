import pytest

from koswat.configuration.settings.koswat_scenario import KoswatScenario
from koswat.configuration.settings.reinforcements.koswat_reinforcement_settings import (
    KoswatReinforcementSettings,
)
from koswat.dike.koswat_input_profile_protocol import KoswatInputProfileProtocol
from koswat.dike_reinforcements.input_profile.input_profile_enum import InputProfileEnum
from koswat.dike_reinforcements.reinforcement_profile.berm_calculator.berm_calculator_result import (
    BermCalculatorResult,
)
from koswat.dike_reinforcements.reinforcement_profile.berm_calculator.no_berm_calculator import (
    NoBermCalculator,
)


class TestNoBermCalculator:
    @pytest.mark.parametrize(
        "profile_type, expected_slope",
        [
            pytest.param(InputProfileEnum.NONE, 0.609091, id="Default"),
            pytest.param(
                InputProfileEnum.STABILITY_WALL, 0.00909091, id="Stability wall"
            ),
        ],
    )
    def test_calculate(
        self,
        valid_scenario: KoswatScenario,
        valid_input_profile: KoswatInputProfileProtocol,
        valid_reinforcement_settings: KoswatReinforcementSettings,
        profile_type: InputProfileEnum,
        expected_slope: float,
    ):
        # 1. Define test data
        _calculator = NoBermCalculator(
            scenario=valid_scenario,
            reinforcement_settings=valid_reinforcement_settings,
            dikebase_piping_old=4.5,
            dikebase_piping_new=5.6,
            dikebase_height_new=6.7,
            dikebase_stability_new=7.8,
            dike_height_new=8.9,
            reinforcement_type=profile_type,
        )

        # 2. Run test
        _result = _calculator.calculate(
            base_data=valid_input_profile,
            reinforced_data=valid_input_profile,
        )

        # 3. Verify expectations
        assert isinstance(_result, BermCalculatorResult)
        assert _result.berm_width == 0.0
        assert _result.berm_height == valid_input_profile.polderside_ground_level
        assert _result.slope == pytest.approx(expected_slope)
