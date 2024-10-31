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
            polderside_berm_width: float
            polderside_ground_level: float

        class MockSettings(KoswatPipingWallSettings):
            min_length_piping_wall: float
            max_length_piping_wall: float

        # 1. Define test data.
        _calculator = PipingWallInputProfileCalculation()
        _profile_data = MockProfile()
        _profile_data.polderside_berm_width = 6
        _profile_data.polderside_ground_level = 1
        _profile_data.pleistocene = -5
        _profile_data.aquifer = -2
        _piping_wall_settings = MockSettings()
        _piping_wall_settings.min_length_piping_wall = 0
        _piping_wall_settings.max_length_piping_wall = 99
        _piping_wall_settings.transition_cbwall_sheetpile = 15
        _soil_polderside_berm_width = 12.5
        _expected_result = (6.1, ConstructionTypeEnum.CB_DAMWAND)

        # 2. Run test.
        _length = _calculator._calculate_length_piping_wall(
            _profile_data, _piping_wall_settings, _soil_polderside_berm_width
        )
        _type = _calculator._determine_construction_type(
            _piping_wall_settings.transition_cbwall_sheetpile, _length
        )
        _result = (_length, _type)

        # 3. Verify Expectations.
        assert _result == _expected_result

    def test_calculate_new_crest_height(self):
        class MockProfile(KoswatInputProfileProtocol):
            crest_height: float

        # 1. Define test data.
        _expected_result = 6.6
        _profile_data = MockProfile()
        _profile_data.crest_height = 4.2
        _scenario = KoswatScenario()
        _scenario.d_h = 2.4

        # 2. Run test.
        _result = PipingWallInputProfileCalculation()._calculate_new_crest_height(
            _profile_data, _scenario
        )

        # 3. Verify Expectations.
        assert _result == _expected_result

    def test_calculate_new_polderside_slope(self):
        class MockProfile(KoswatInputProfileProtocol):
            crest_height: float
            crest_width: float
            polderside_slope: float
            polderside_ground_level: float

        # 1. Define test data.
        _expected_value = 3.57
        _scenario = KoswatScenario()
        _scenario.d_h = 1
        _scenario.d_s = 10
        _scenario.d_p = 30
        _scenario.crest_width = 5
        _scenario.waterside_slope = 3
        _input_profile = MockProfile()
        _input_profile.crest_width = 5
        _input_profile.crest_height = 8
        _input_profile.polderside_slope = 3
        _input_profile.polderside_ground_level = 2

        # 2. Run test
        _new_polderside_slope = (
            PipingWallInputProfileCalculation()._calculate_new_polderside_slope(
                _input_profile, _scenario
            )
        )

        # 3. Verify expectations
        assert _new_polderside_slope == pytest.approx(_expected_value, 0.001)
