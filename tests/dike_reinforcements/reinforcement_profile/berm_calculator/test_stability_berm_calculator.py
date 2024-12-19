import pytest

from koswat.dike.koswat_input_profile_protocol import KoswatInputProfileProtocol
from koswat.dike_reinforcements.reinforcement_profile.berm_calculator.berm_calculator_result import (
    BermCalculatorResult,
)
from koswat.dike_reinforcements.reinforcement_profile.berm_calculator.stability_berm_calculator import (
    StabilityBermCalculator,
)


class TestStabilityBermCalculator:
    def test_calculate(self, valid_input_profile: KoswatInputProfileProtocol):
        # 1. Define test data
        _calculator = StabilityBermCalculator(
            scenario=None,
            reinforcement_settings=None,
            dikebase_piping_old=4.5,
            dikebase_piping_new=5.6,
            dikebase_height_new=6.7,
            dikebase_stability_new=7.8,
            dike_height_new=8.9,
            berm_factor_old=0.5,
        )

        # 2. Run test
        _result = _calculator.calculate(
            base_data=valid_input_profile,
            reinforced_data=None,
        )

        # 3. Verify expectations
        assert isinstance(_result, BermCalculatorResult)
        assert _result.berm_width == pytest.approx(1.1)
        assert _result.berm_height == pytest.approx(5.45)
        assert _result.slope == valid_input_profile.polderside_slope
