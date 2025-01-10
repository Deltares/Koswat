from koswat.dike.koswat_input_profile_protocol import KoswatInputProfileProtocol
from koswat.dike_reinforcements.reinforcement_profile.berm_calculator.berm_calculator_result import (
    BermCalculatorResult,
)
from koswat.dike_reinforcements.reinforcement_profile.berm_calculator.default_berm_calculator import (
    DefaultBermCalculator,
)


class TestDefaultCalculator:
    def test_calculate(self, valid_input_profile: KoswatInputProfileProtocol):
        # 1. Define test data
        _calculator = DefaultBermCalculator(
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
        assert _result.berm_width == 0.0
        assert _result.berm_height == valid_input_profile.polderside_ground_level
        assert _result.slope == valid_input_profile.polderside_slope
