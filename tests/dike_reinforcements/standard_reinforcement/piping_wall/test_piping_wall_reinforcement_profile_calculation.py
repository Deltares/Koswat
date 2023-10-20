import pytest

from koswat.dike_reinforcements.input_profile.reinforcement_input_profile_calculation_protocol import (
    ReinforcementInputProfileCalculationProtocol,
)
from koswat.dike_reinforcements.input_profile.piping_wall.piping_wall_input_profile_calculation import (
    PipingWallReinforcementProfileCalculation,
)
from koswat.configuration.settings import KoswatScenario
from koswat.core.protocols import BuilderProtocol
from koswat.dike.koswat_input_profile_protocol import KoswatInputProfileProtocol


class TestPipingWallReinforcementProfileCalculation:
    def test_initialize(self):
        _calculation = PipingWallReinforcementProfileCalculation()
        assert _calculation
        assert not _calculation.base_profile
        assert not _calculation.scenario
        assert isinstance(_calculation, PipingWallReinforcementProfileCalculation)
        assert isinstance(_calculation, ReinforcementInputProfileCalculationProtocol)
        assert isinstance(_calculation, BuilderProtocol)

    def test_calculate_length_stability_wall(self):
        class MockProfile(KoswatInputProfileProtocol):
            binnen_berm_breedte: float

        # 1. Define test data.
        _calculator = PipingWallReinforcementProfileCalculation()
        _profile_data = MockProfile()
        _profile_data.binnen_berm_breedte = 6
        _expected_result = 2.5

        # 2. Run test.
        _result = _calculator._calculate_length_piping_wall(_profile_data)

        # 3. Verify Expectations.
        assert _result == _expected_result

    def test_calculate_length_stability_wall(self):
        class MockProfile(KoswatInputProfileProtocol):
            kruin_hoogte: float

        # 1. Define test data.
        _expected_result = 6.6
        _profile_data = MockProfile()
        _profile_data.kruin_hoogte = 4.2
        _scenario = KoswatScenario()
        _scenario.d_h = 2.4

        # 2. Run test.
        _result = (
            PipingWallReinforcementProfileCalculation()._calculate_new_kruin_hoogte(
                _profile_data, _scenario
            )
        )

        # 3. Verify Expectations.
        assert _result == _expected_result

    def test_calculate_new_binnen_talud(self):
        class MockProfile(KoswatInputProfileProtocol):
            kruin_hoogte: float
            kruin_breedte: float
            binnen_talud: float
            binnen_maaiveld: float

        # 1. Define test data.
        _expected_value = 3.57
        _scenario = KoswatScenario()
        _scenario.d_h = 1
        _scenario.d_s = 10
        _scenario.d_p = 30
        _scenario.kruin_breedte = 5
        _scenario.buiten_talud = 3
        _input_profile = MockProfile()
        _input_profile.kruin_breedte = 5
        _input_profile.kruin_hoogte = 8
        _input_profile.binnen_talud = 3
        _input_profile.binnen_maaiveld = 2

        # 2. Run test
        _new_binnen_talud = (
            PipingWallReinforcementProfileCalculation()._calculate_new_binnen_talud(
                _input_profile, _scenario
            )
        )

        # 3. Verify expectations
        assert _new_binnen_talud == pytest.approx(_expected_value, 0.001)
