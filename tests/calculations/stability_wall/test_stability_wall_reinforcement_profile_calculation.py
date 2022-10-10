from koswat.builder_protocol import BuilderProtocol
from koswat.calculations.reinforcement_profile_calculation_protocol import (
    ReinforcementProfileCalculationProtocol,
)
from koswat.calculations.stability_wall.stability_wall_reinforcement_profile_calculation import (
    StabilityWallReinforcementProfileCalculation,
)
from koswat.dike.koswat_input_profile_protocol import KoswatInputProfileProtocol
from koswat.koswat_scenario import KoswatScenario


class TestStabilityWallReinforcementProfileCalculation:
    def test_initialize(self):
        _calculation = StabilityWallReinforcementProfileCalculation()
        assert _calculation
        assert not _calculation.base_profile
        assert not _calculation.scenario
        assert isinstance(_calculation, StabilityWallReinforcementProfileCalculation)
        assert isinstance(_calculation, ReinforcementProfileCalculationProtocol)
        assert isinstance(_calculation, BuilderProtocol)

    def test_calculate_length_stability_wall(self):
        class MockInputData(KoswatInputProfileProtocol):
            kruin_hoogte: float

        # 1. Define test data.
        _calculator = StabilityWallReinforcementProfileCalculation()
        _input_data = MockInputData()
        _input_data.kruin_hoogte = 17
        _scenario = KoswatScenario()
        _scenario.d_h = 16
        _expected_result = 42

        # 2. Run test.
        _result = _calculator._calculate_length_stability_wall(_input_data, _scenario)

        # 3. Verify expectations
        assert _result == _expected_result

    def test_calculate_new_kruin_hoogte(self):
        class MockInputData(KoswatInputProfileProtocol):
            kruin_hoogte: float

        # 1. Define test data.
        _calculator = StabilityWallReinforcementProfileCalculation()
        _input_data = MockInputData()
        _input_data.kruin_hoogte = 30
        _scenario = KoswatScenario()
        _scenario.d_h = 12
        _expected_result = 42

        # 2. Run test.
        _result = _calculator._calculate_new_kruin_hoogte(_input_data, _scenario)

        # 3. Verify expectations
        assert _result == _expected_result

    def test_calculate_new_binnen_talud(self):
        class MockInputData(KoswatInputProfileProtocol):
            kruin_hoogte: float

        # 1. Define test data.
        _calculator = StabilityWallReinforcementProfileCalculation()
        _input_data = MockInputData()
        _input_data.kruin_hoogte = 30
        _input_data.binnen_maaiveld = 2.3
        _input_data.binnen_talud = 4.5
        _input_data.kruin_breedte = 5.6
        _scenario = KoswatScenario()
        _scenario.d_h = 12
        _scenario.kruin_breedte = 6.7
        _scenario.buiten_talud = 7.8
        _expected_result = 2

        # 2. Run test.
        _result = _calculator._calculate_new_binnen_talud(_input_data, _scenario)

        # 3. Verify expectations
        assert _result == _expected_result
