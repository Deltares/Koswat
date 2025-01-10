from dataclasses import dataclass

import pytest

from koswat.configuration.settings import KoswatScenario
from koswat.configuration.settings.koswat_general_settings import ConstructionTypeEnum
from koswat.configuration.settings.reinforcements.koswat_piping_wall_settings import (
    KoswatPipingWallSettings,
)
from koswat.configuration.settings.reinforcements.koswat_reinforcement_settings import (
    KoswatReinforcementSettings,
)
from koswat.core.protocols import BuilderProtocol
from koswat.dike.koswat_input_profile_protocol import KoswatInputProfileProtocol
from koswat.dike.profile.koswat_input_profile_base import KoswatInputProfileBase
from koswat.dike_reinforcements.input_profile.piping_wall.piping_wall_input_profile import (
    PipingWallInputProfile,
)
from koswat.dike_reinforcements.input_profile.piping_wall.piping_wall_input_profile_calculation import (
    PipingWallInputProfileCalculation,
)
from koswat.dike_reinforcements.input_profile.reinforcement_input_profile_calculation_protocol import (
    ReinforcementInputProfileCalculationProtocol,
)
from koswat.dike_reinforcements.reinforcement_profile.reinforcement_profile import (
    ReinforcementProfile,
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

    @pytest.mark.parametrize(
        "seepage_length, expected",
        [
            pytest.param(0.0, 0.0, id="seepage_lenght=0.0"),
            pytest.param(30.0, 9.0, id="seepage_length=30.0"),
        ],
    )
    def test__calculate_length_piping_wall(
        self, seepage_length: float, expected: float
    ):
        @dataclass
        class MockProfile(KoswatInputProfileProtocol):
            polderside_ground_level: float
            aquifer: float

        @dataclass
        class MockSettings(KoswatPipingWallSettings):
            min_length_piping_wall: float
            max_length_piping_wall: float

        # 1. Define test data.
        _calculator = PipingWallInputProfileCalculation()
        _profile_data = MockProfile(
            polderside_ground_level=1,
            aquifer=-2,
        )
        _piping_wall_settings = MockSettings(
            min_length_piping_wall=0,
            max_length_piping_wall=99,
        )

        # 2. Run test.
        _result = _calculator._calculate_length_piping_wall(
            _profile_data, _piping_wall_settings, seepage_length
        )

        # 3. Verify Expectations.
        assert _result == expected

    @pytest.mark.parametrize(
        "construction_length, expected",
        [
            pytest.param(0.0, None, id="length = 0"),
            pytest.param(
                10.0,
                ConstructionTypeEnum.CB_DAMWAND,
                id="0 < length < transition",
            ),
            pytest.param(
                20.0, ConstructionTypeEnum.DAMWAND_ONVERANKERD, id="length > transition"
            ),
        ],
    )
    def test__calculate_construction_type(
        self, construction_length: float, expected: ConstructionTypeEnum | None
    ):
        # 1. Define test data.
        _transition = 15.0

        # 2. Run test
        _result = PipingWallInputProfileCalculation._determine_construction_type(
            _transition, construction_length
        )

        # 3. Verify expectations
        assert _result == expected

    def test_build(self, valid_input_data: KoswatInputProfileProtocol):
        @dataclass
        class MockSettings(KoswatPipingWallSettings):
            min_length_piping_wall: float
            max_length_piping_wall: float
            transition_cbwall_sheetpile: float

        # 1. Define test data.
        _calculator = PipingWallInputProfileCalculation()
        _calculator.base_profile = ReinforcementProfile(input_data=valid_input_data)
        _reinforcement_settings = KoswatReinforcementSettings(
            piping_wall_settings=MockSettings(
                min_length_piping_wall=0,
                max_length_piping_wall=99,
                transition_cbwall_sheetpile=15,
            )
        )
        _calculator.reinforcement_settings = _reinforcement_settings
        _calculator.scenario = KoswatScenario(
            d_h=12.0, crest_width=6.7, waterside_slope=7.8
        )

        # 2. Run test.
        _result = _calculator.build()

        # 3. Verify Expectations.
        assert isinstance(_result, PipingWallInputProfile)
        assert isinstance(_result, KoswatInputProfileBase)
        assert isinstance(_result, KoswatInputProfileProtocol)

        assert _result.dike_section == "mocked_section"
        assert _result.waterside_ground_level == 6.7
        assert _result.waterside_slope == 7.8
        assert _result.waterside_berm_height == 19.8
        assert _result.waterside_berm_width == 8.9
        assert _result.crest_height == 42
        assert _result.crest_width == 6.7
        assert _result.polderside_slope == 4.5
        assert _result.polderside_berm_height == 2.3
        assert _result.polderside_berm_width == 0.0
        assert _result.polderside_ground_level == 2.3
        assert _result.ground_price_builtup == 150
        assert _result.ground_price_unbuilt == 10
        assert _result.factor_settlement == 1.2
        assert _result.pleistocene == -6.7
        assert _result.aquifer == -2.3
