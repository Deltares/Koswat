from koswat.builder_protocol import BuilderProtocol
from koswat.calculations.reinforcement_profile_calculation_protocol import (
    ReinforcementInputProfileCalculationProtocol,
)
from koswat.calculations.standard_reinforcement.stability_wall.stability_wall_input_profile import (
    StabilityWallInputProfile,
)
from koswat.calculations.standard_reinforcement.stability_wall.stability_wall_reinforcement_profile_calculation import (
    StabilityWallReinforcementProfileCalculation,
)
from koswat.configuration.settings import KoswatScenario
from koswat.dike.koswat_input_profile_protocol import KoswatInputProfileProtocol
from koswat.dike.profile.koswat_input_profile_base import KoswatInputProfileBase


class TestStabilityWallReinforcementProfileCalculation:
    def test_initialize(self):
        _calculation = StabilityWallReinforcementProfileCalculation()
        assert _calculation
        assert not _calculation.base_profile
        assert not _calculation.scenario
        assert isinstance(_calculation, StabilityWallReinforcementProfileCalculation)
        assert isinstance(_calculation, ReinforcementInputProfileCalculationProtocol)
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
            binnen_maaiveld: float
            binnen_talud: float
            kruin_breedte: float

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

    def test_calculate_new_input_profile(self):
        class MockInputData(KoswatInputProfileProtocol):
            dike_section: str
            kruin_hoogte: float
            binnen_maaiveld: float
            binnen_talud: float
            kruin_breedte: float
            buiten_berm_breedte: float

        # 1. Define test data.
        _calculator = StabilityWallReinforcementProfileCalculation()
        _input_data = MockInputData()
        _input_data.dike_section = "mocked_section"
        _input_data.kruin_hoogte = 30
        _input_data.binnen_maaiveld = 2.3
        _input_data.binnen_talud = 4.5
        _input_data.kruin_breedte = 5.6
        _input_data.buiten_maaiveld = 6.7
        _input_data.buiten_berm_hoogte = 7.8
        _input_data.buiten_berm_breedte = 8.9
        _scenario = KoswatScenario()
        _scenario.d_h = 12
        _scenario.kruin_breedte = 6.7
        _scenario.buiten_talud = 7.8

        # 2. Run test.
        _result = _calculator._calculate_new_input_profile(_input_data, _scenario)

        # 3. Verify expectations
        assert isinstance(_result, StabilityWallInputProfile)
        assert isinstance(_result, KoswatInputProfileBase)
        assert isinstance(_result, KoswatInputProfileProtocol)
