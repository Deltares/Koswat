import pytest

from koswat.configuration.settings import KoswatScenario
from koswat.configuration.settings.koswat_general_settings import ConstructionTypeEnum
from koswat.configuration.settings.reinforcements.koswat_stability_wall_settings import (
    KoswatStabilityWallSettings,
)
from koswat.core.protocols import BuilderProtocol
from koswat.dike.koswat_input_profile_protocol import KoswatInputProfileProtocol
from koswat.dike.profile.koswat_input_profile_base import KoswatInputProfileBase
from koswat.dike_reinforcements.input_profile import StabilityWallInputProfile
from koswat.dike_reinforcements.input_profile.reinforcement_input_profile_calculation_protocol import (
    ReinforcementInputProfileCalculationProtocol,
)
from koswat.dike_reinforcements.input_profile.stability_wall.stability_wall_input_profile_calculation import (
    StabilityWallInputProfileCalculation,
)


class TestStabilityWallInputProfileCalculation:
    def test_initialize(self):
        _calculation = StabilityWallInputProfileCalculation()
        assert _calculation
        assert not _calculation.base_profile
        assert not _calculation.scenario
        assert isinstance(_calculation, StabilityWallInputProfileCalculation)
        assert isinstance(_calculation, ReinforcementInputProfileCalculationProtocol)
        assert isinstance(_calculation, BuilderProtocol)

    @pytest.mark.parametrize(
        "soil_polderside_berm_width, expected",
        [
            pytest.param(
                0,
                (13.5, ConstructionTypeEnum.DAMWAND_VERANKERD),
                id="soil_polderside_berm_width=0",
            ),
            pytest.param(
                30.0,
                (14.5, ConstructionTypeEnum.DIEPWAND),
                id="soil_polderside_berm_width=30",
            ),
        ],
    )
    def test_calculate_length_type_stability_wall(
        self,
        soil_polderside_berm_width: float,
        expected: tuple[float, ConstructionTypeEnum],
    ):
        class MockInputData(KoswatInputProfileProtocol):
            pleistocene: float
            aquifer: float

        class MockSettings(KoswatStabilityWallSettings):
            min_length_stability_wall: float
            max_length_stability_wall: float

        # 1. Define test data.
        _calculator = StabilityWallInputProfileCalculation()
        _input_data = MockInputData()
        _input_data.pleistocene = -5
        _input_data.aquifer = -2
        _stability_wall_settings = MockSettings()
        _stability_wall_settings.min_length_stability_wall = 0
        _stability_wall_settings.max_length_stability_wall = 99
        _stability_wall_settings.transition_sheetpile_diaphragm_wall = 14
        _soil_polderside_berm_width = soil_polderside_berm_width
        _new_crest_height = 8

        # 2. Run test.
        _length = _calculator._calculate_length_stability_wall(
            _input_data,
            _stability_wall_settings,
            _soil_polderside_berm_width,
            _new_crest_height,
        )
        _type = _calculator._determine_construction_type(
            _stability_wall_settings.transition_sheetpile_diaphragm_wall, _length
        )
        _result = (_length, _type)

        # 3. Verify expectations
        assert _result == expected

    def test_calculate_new_crest_height(self):
        class MockInputData(KoswatInputProfileProtocol):
            crest_height: float

        # 1. Define test data.
        _calculator = StabilityWallInputProfileCalculation()
        _input_data = MockInputData()
        _input_data.crest_height = 30
        _scenario = KoswatScenario()
        _scenario.d_h = 12
        _expected_result = 42

        # 2. Run test.
        _result = _calculator._calculate_new_crest_height(_input_data, _scenario)

        # 3. Verify expectations
        assert _result == _expected_result

    def test_calculate_new_polderside_slope(self):
        class MockInputData(KoswatInputProfileProtocol):
            crest_height: float
            polderside_ground_level: float
            polderside_slope: float
            crest_width: float

        # 1. Define test data.
        _calculator = StabilityWallInputProfileCalculation()
        _input_data = MockInputData()
        _input_data.crest_height = 30
        _input_data.polderside_ground_level = 2.3
        _input_data.polderside_slope = 4.5
        _input_data.crest_width = 5.6
        _scenario = KoswatScenario()
        _scenario.d_h = 12
        _scenario.crest_width = 6.7
        _scenario.waterside_slope = 7.8
        _expected_result = 2

        # 2. Run test.
        _result = _calculator._calculate_new_polderside_slope(_input_data, _scenario)

        # 3. Verify expectations
        assert _result == _expected_result

    def test_calculate_new_input_profile(self):
        class MockInputData(KoswatInputProfileProtocol):
            dike_section: str
            crest_height: float
            polderside_berm_width: float
            polderside_ground_level: float
            polderside_slope: float
            crest_width: float
            waterside_berm_width: float
            waterside_slope: float
            ground_price_builtup: float
            ground_price_unbuilt: float
            factor_settlement: float
            pleistocene: float
            aquifer: float

        class MockSettings(KoswatStabilityWallSettings):
            min_length_stability_wall: float
            max_length_stability_wall: float

        # 1. Define test data.
        _calculator = StabilityWallInputProfileCalculation()
        _input_data = MockInputData()
        _input_data.dike_section = "mocked_section"
        _input_data.crest_height = 30
        _input_data.polderside_berm_width = 8.9
        _input_data.polderside_ground_level = 2.3
        _input_data.polderside_slope = 4.5
        _input_data.crest_width = 5.6
        _input_data.waterside_ground_level = 6.7
        _input_data.waterside_berm_height = 7.8
        _input_data.waterside_berm_width = 8.9
        _input_data.waterside_slope = 3.4
        _input_data.ground_price_builtup = 150
        _input_data.ground_price_unbuilt = 10
        _input_data.factor_settlement = 1.2
        _input_data.pleistocene = -6.7
        _input_data.aquifer = -2.3
        _stability_wall_settings = MockSettings()
        _stability_wall_settings.min_length_stability_wall = 0
        _stability_wall_settings.max_length_stability_wall = 99
        _scenario = KoswatScenario()
        _scenario.d_h = 12
        _scenario.crest_width = 6.7
        _scenario.waterside_slope = 7.8

        # 2. Run test.
        _result = _calculator._calculate_new_input_profile(
            _input_data, _stability_wall_settings, _scenario
        )

        # 3. Verify expectations
        assert isinstance(_result, StabilityWallInputProfile)
        assert isinstance(_result, KoswatInputProfileBase)
        assert isinstance(_result, KoswatInputProfileProtocol)
