from koswat.dike.koswat_input_profile_protocol import KoswatInputProfileProtocol
from koswat.dike_reinforcements.reinforcement_profile.berm_calculator.default_berm_calculator import (
    DefaultBermCalculator,
)


class TestDefaultCalculator:
    def test_calculate(self, valid_input_profile: KoswatInputProfileProtocol):
        # 1. Define test data
        _calculator = DefaultBermCalculator(
            dikebase_piping_old=0,
            dikebase_piping_new=0,
            dike_height_new=0,
        )

        # 2. Run test
        _result = _calculator.calculate(
            base_data=valid_input_profile,
            reinforced_data=valid_input_profile,
        )

        # 3. Verify expectations
        assert isinstance(_result, tuple)
        assert len(_result) == 3
        assert all(isinstance(_, float) for _ in _result)
        assert _result[0] == 0.0
        assert _result[1] == valid_input_profile.polderside_ground_level
        assert _result[2] == valid_input_profile.polderside_slope
