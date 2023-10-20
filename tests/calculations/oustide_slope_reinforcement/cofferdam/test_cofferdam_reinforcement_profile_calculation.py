import pytest

from koswat.dike_reinforcements.reinforcement_profiles.outside_slope_reinforcement.cofferdam.cofferdam_input_profile import (
    CofferDamInputProfile,
)
from koswat.dike_reinforcements.reinforcement_profiles.outside_slope_reinforcement.cofferdam.cofferdam_reinforcement_profile_calculation import (
    CofferdamReinforcementProfileCalculation,
)
from koswat.dike_reinforcements.reinforcement_profiles.reinforcement_input_profile_calculation_protocol import (
    ReinforcementInputProfileCalculationProtocol,
)
from koswat.configuration.settings import KoswatScenario
from koswat.dike.koswat_input_profile_protocol import KoswatInputProfileProtocol
from koswat.dike.profile.koswat_input_profile_base import KoswatInputProfileBase


class TestCofferDamReinforcementProfileCalculation:
    def test_initialize(self):
        _calculation = CofferdamReinforcementProfileCalculation()
        assert _calculation
        assert not _calculation.base_profile
        assert not _calculation.scenario
        assert isinstance(_calculation, CofferdamReinforcementProfileCalculation)
        assert isinstance(_calculation, ReinforcementInputProfileCalculationProtocol)

    def test_calculate_length_coffer_dam(self):
        class MockInputData(KoswatInputProfileProtocol):
            kruin_hoogte: float
            binnen_maaiveld: float

        # 1. Define test data.
        _calculator = CofferdamReinforcementProfileCalculation()
        _input_data = MockInputData()
        _input_data.kruin_hoogte = 8
        _input_data.binnen_maaiveld = 2
        _scenario = KoswatScenario()
        _scenario.d_h = 2
        _expected_result = 17

        # 2. Run test.
        _result = _calculator._calculate_new_length_coffer_dam(_input_data, _scenario)

        # 3. Verify expectations
        assert _result == _expected_result

    def test_calculate_new_kruin_hoogte(self):
        class MockInputData(KoswatInputProfileProtocol):
            kruin_hoogte: float

        # 1. Define test data.
        _calculator = CofferdamReinforcementProfileCalculation()
        _input_data = MockInputData()
        _input_data.kruin_hoogte = 6
        _scenario = KoswatScenario()
        _scenario.d_h = 2
        _expected_result = 8

        # 2. Run test.
        _result = _calculator._calculate_new_kruin_hoogte(_input_data, _scenario)

        # 3. Verify expectations
        assert _result == _expected_result

    def test_calculate_new_buiten_talud(self):
        class MockInputData(KoswatInputProfileProtocol):
            kruin_hoogte: float
            buiten_talud: float
            buiten_maaiveld: float

        # 1. Define test data.
        _calculator = CofferdamReinforcementProfileCalculation()
        _input_data = MockInputData()
        _input_data.kruin_hoogte = 8
        _input_data.buiten_maaiveld = 2
        _input_data.buiten_talud = 3
        _scenario = KoswatScenario()
        _scenario.d_h = 2
        _expected_result = 2.25

        # 2. Run test.
        _result = _calculator._calculate_new_buiten_talud(_input_data, _scenario)

        # 3. Verify expectations
        assert _result == _expected_result

    def test_calculate_new_binnen_talud(self):
        class MockInputData(KoswatInputProfileProtocol):
            kruin_breedte: float
            kruin_hoogte: float
            binnen_maaiveld: float
            binnen_talud: float

        # 1. Define test data.
        _expected_result = 2.25
        _calculator = CofferdamReinforcementProfileCalculation()
        _input_data = MockInputData()
        _input_data.kruin_hoogte = 6
        _input_data.binnen_maaiveld = 0
        _input_data.binnen_talud = 3
        _input_data.kruin_breedte = 5
        _scenario = KoswatScenario()
        _scenario.d_h = 2
        _scenario.kruin_breedte = 5
        _scenario.buiten_talud = 3

        # 2. Run test.
        _result = _calculator._calculate_new_binnen_talud(_input_data, _scenario)

        # 3. Verify expectations
        assert _result == pytest.approx(_expected_result, 0.001)

    def test_calculate_new_input_profile(self):
        class MockInputData(KoswatInputProfileProtocol):
            dike_section: str
            kruin_hoogte: float
            binnen_maaiveld: float
            binnen_talud: float
            kruin_breedte: float
            buiten_berm_breedte: float
            buiten_talud: float

        # 1. Define test data.
        _calculator = CofferdamReinforcementProfileCalculation()
        _input_data = MockInputData()
        _input_data.dike_section = "mocked_section"
        _input_data.kruin_hoogte = 30
        _input_data.binnen_maaiveld = 2.3
        _input_data.binnen_talud = 4.5
        _input_data.kruin_breedte = 5.6
        _input_data.buiten_maaiveld = 6.7
        _input_data.buiten_berm_hoogte = 7.8
        _input_data.buiten_berm_breedte = 8.9
        _input_data.buiten_talud = 9.9
        _scenario = KoswatScenario()
        _scenario.d_h = 12
        _scenario.kruin_breedte = 6.7
        _scenario.buiten_talud = 7.8

        # 2. Run test.
        _result = _calculator._calculate_new_input_profile(_input_data, _scenario)

        # 3. Verify expectations
        assert isinstance(_result, CofferDamInputProfile)
        assert isinstance(_result, KoswatInputProfileBase)
        assert isinstance(_result, KoswatInputProfileProtocol)
