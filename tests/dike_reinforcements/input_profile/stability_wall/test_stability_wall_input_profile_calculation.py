from dataclasses import dataclass

import pytest

from koswat.configuration.settings import KoswatScenario
from koswat.configuration.settings.koswat_general_settings import ConstructionTypeEnum
from koswat.configuration.settings.reinforcements.koswat_reinforcement_settings import (
    KoswatReinforcementSettings,
)
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
from koswat.dike_reinforcements.reinforcement_profile.reinforcement_profile import (
    ReinforcementProfile,
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
        "seepage_length, stab_wall, expected",
        [
            pytest.param(
                0.0,
                True,
                13.5,
                id="seepage_length=0_stab_wall=True",
            ),
            pytest.param(
                0.0,
                False,
                0.0,
                id="seepage_length=0_stab_wall=False",
            ),
            pytest.param(
                30.0,
                True,
                14.5,
                id="seepage_length=30_stab_wall=True",
            ),
            pytest.param(
                30.0,
                False,
                9.0,
                id="seepage_length=30_stab_wall=False",
            ),
        ],
    )
    def test__calculate_length_stability_wall(
        self,
        seepage_length: float,
        stab_wall: bool,
        expected: float,
    ):
        @dataclass
        class MockInputData(KoswatInputProfileProtocol):
            polderside_ground_level: float
            pleistocene: float
            aquifer: float

        @dataclass
        class MockSettings(KoswatStabilityWallSettings):
            min_length_stability_wall: float
            max_length_stability_wall: float

        # 1. Define test data.
        _input_data = MockInputData(
            polderside_ground_level=1.0, pleistocene=-5.0, aquifer=-2.0
        )
        _stability_wall_settings = MockSettings(
            min_length_stability_wall=0,
            max_length_stability_wall=99,
        )
        _new_crest_height = 8

        # 2. Run test.
        _result = StabilityWallInputProfileCalculation._calculate_length_stability_wall(
            _input_data,
            _stability_wall_settings,
            seepage_length,
            stab_wall,
            _new_crest_height,
        )

        # 3. Verify expectations
        assert _result == expected

    @pytest.mark.parametrize(
        "construction_length, expected",
        [
            pytest.param(0.0, None, id="length = 0"),
            pytest.param(
                10.0,
                ConstructionTypeEnum.DAMWAND_VERANKERD,
                id="0 < length < transition",
            ),
            pytest.param(20.0, ConstructionTypeEnum.DIEPWAND, id="length > transition"),
        ],
    )
    def test__determine_construction_type(
        self, construction_length: float, expected: ConstructionTypeEnum | None
    ):
        # 1. Define test data.
        _transition = 15.0

        # 2. Run test
        _result = StabilityWallInputProfileCalculation._determine_construction_type(
            _transition, construction_length
        )

        # 3. Verify expectations
        assert _result == expected

    def test_build(self, valid_input_data: KoswatInputProfileProtocol):
        @dataclass
        class MockSettings(KoswatStabilityWallSettings):
            min_length_stability_wall: float
            max_length_stability_wall: float
            transition_sheetpile_diaphragm_wall: float

        # 1. Define test data.
        _calculator = StabilityWallInputProfileCalculation()
        _calculator.base_profile = ReinforcementProfile(input_data=valid_input_data)
        _reinforcement_settings = KoswatReinforcementSettings(
            stability_wall_settings=MockSettings(
                min_length_stability_wall=0,
                max_length_stability_wall=99,
                transition_sheetpile_diaphragm_wall=15,
            )
        )
        _calculator.reinforcement_settings = _reinforcement_settings
        _calculator.scenario = KoswatScenario(
            d_h=12.0, crest_width=6.7, waterside_slope=7.8
        )

        # 2. Run test.
        _result = _calculator.build()

        # 3. Verify expectations
        assert isinstance(_result, StabilityWallInputProfile)
        assert isinstance(_result, KoswatInputProfileBase)
        assert isinstance(_result, KoswatInputProfileProtocol)

        assert _result.dike_section == "mocked_section"
        assert _result.waterside_ground_level == 6.7
        assert _result.waterside_slope == 7.8
        assert _result.waterside_berm_height == 19.8
        assert _result.waterside_berm_width == 8.9
        assert _result.crest_height == 42
        assert _result.crest_width == 6.7
        assert _result.polderside_slope == pytest.approx(0.981108)
        assert _result.polderside_berm_height == 2.3
        assert _result.polderside_berm_width == 0.0
        assert _result.polderside_ground_level == 2.3
        assert _result.ground_price_builtup == 150
        assert _result.ground_price_unbuilt == 10
        assert _result.factor_settlement == 1.2
        assert _result.pleistocene == -6.7
        assert _result.aquifer == -2.3
