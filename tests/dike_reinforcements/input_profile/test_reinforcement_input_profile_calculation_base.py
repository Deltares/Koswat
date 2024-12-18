from koswat.configuration.settings.koswat_scenario import KoswatScenario
from koswat.dike.koswat_input_profile_protocol import KoswatInputProfileProtocol
from koswat.dike_reinforcements.input_profile.reinforcement_input_profile_calculation_base import (
    ReinforcementInputProfileCalculationBase,
)


class TestReinforcementInputProfileCalculationBase:
    def test_populate_profile(self):
        pass

    def test__calculate_new_waterside_slope(self):
        # 1. Define test data.
        _waterside_slope = 3.0
        _scenario = KoswatScenario(waterside_slope=_waterside_slope)

        # 2. Run test.
        _result = ReinforcementInputProfileCalculationBase._calculate_new_crest_height(
            None, _scenario
        )

        # 3. Verify expectations
        assert _result == _waterside_slope

    def test__calculate_new_crest_height(self):
        class MockInputData(KoswatInputProfileProtocol):
            crest_height: float

        # 1. Define test data.
        _input_data = MockInputData()
        _input_data.crest_height = 6
        _scenario = KoswatScenario()
        _scenario.d_h = 2
        _expected_result = 8

        # 2. Run test.
        _result = ReinforcementInputProfileCalculationBase._calculate_new_crest_height(
            _input_data, _scenario
        )

        # 3. Verify expectations
        assert _result == _expected_result

    def test___calculate_new_waterside_berm_height(self):
        pass

    def test__calculate_new_polderside_berm_height_piping(self):
        pass
