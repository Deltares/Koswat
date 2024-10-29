import pytest

from koswat.configuration.settings import KoswatScenario
from koswat.configuration.settings.koswat_general_settings import ConstructionTypeEnum
from koswat.configuration.settings.reinforcements.koswat_piping_wall_settings import (
    KoswatPipingWallSettings,
)
from koswat.core.protocols import BuilderProtocol
from koswat.dike.koswat_input_profile_protocol import KoswatInputProfileProtocol
from koswat.dike_reinforcements.input_profile.piping_wall.piping_wall_input_profile_calculation import (
    PipingWallInputProfileCalculation,
)
from koswat.dike_reinforcements.input_profile.reinforcement_input_profile_calculation_protocol import (
    ReinforcementInputProfileCalculationProtocol,
)


class TestPipingWallInputProfileCalculation:
    def test_initialize(self):
        _calculation = PipingWallInputProfileCalculation()
        assert _calculation
        assert not _calculation.base_profile
        assert not _calculation.scenario
        assert isinstance(_calculation, PipingWallInputProfileCalculation)
        assert isinstance(_calculation, ReinforcementInputProfileCalculationProtocol)
        assert isinstance(_calculation, BuilderProtocol)

    def test_calculate_length_type_piping_wall(self):
        class MockProfile(KoswatInputProfileProtocol):
            binnen_berm_breedte: float
            binnen_maaiveld: float

        class MockSettings(KoswatPipingWallSettings):
            min_lengte_kwelscherm: float
            max_lengte_kwelscherm: float

        # 1. Define test data.
        _calculator = PipingWallInputProfileCalculation()
        _profile_data = MockProfile()
        _profile_data.binnen_berm_breedte = 6
        _profile_data.binnen_maaiveld = 1
        _profile_data.pleistoceen = -5
        _profile_data.aquifer = -2
        _piping_wall_settings = MockSettings()
        _piping_wall_settings.min_lengte_kwelscherm = 0
        _piping_wall_settings.max_lengte_kwelscherm = 99
        _piping_wall_settings.transition_cbwall_sheet_pile = 15
        _soil_binnen_berm_breedte = 12.5
        _expected_result = (6.1, ConstructionTypeEnum.CB_DAMWAND)

        # 2. Run test.
        _length = _calculator._calculate_length_piping_wall(
            _profile_data, _piping_wall_settings, _soil_binnen_berm_breedte
        )
        _type = _calculator._determine_construction_type(
            _piping_wall_settings.transition_cbwall_sheet_pile, _length
        )
        _result = (_length, _type)

        # 3. Verify Expectations.
        assert _result == _expected_result

    def test_calculate_new_kruin_hoogte(self):
        class MockProfile(KoswatInputProfileProtocol):
            kruin_hoogte: float

        # 1. Define test data.
        _expected_result = 6.6
        _profile_data = MockProfile()
        _profile_data.kruin_hoogte = 4.2
        _scenario = KoswatScenario()
        _scenario.d_h = 2.4

        # 2. Run test.
        _result = PipingWallInputProfileCalculation()._calculate_new_kruin_hoogte(
            _profile_data, _scenario
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
            PipingWallInputProfileCalculation()._calculate_new_binnen_talud(
                _input_profile, _scenario
            )
        )

        # 3. Verify expectations
        assert _new_binnen_talud == pytest.approx(_expected_value, 0.001)
