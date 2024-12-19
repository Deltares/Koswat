from dataclasses import dataclass

import pytest

from koswat.configuration.settings import KoswatScenario
from koswat.configuration.settings.koswat_general_settings import ConstructionTypeEnum
from koswat.configuration.settings.reinforcements.koswat_cofferdam_settings import (
    KoswatCofferdamSettings,
)
from koswat.configuration.settings.reinforcements.koswat_reinforcement_settings import (
    KoswatReinforcementSettings,
)
from koswat.dike.koswat_input_profile_protocol import KoswatInputProfileProtocol
from koswat.dike.profile.koswat_input_profile_base import KoswatInputProfileBase
from koswat.dike_reinforcements.input_profile.cofferdam.cofferdam_input_profile import (
    CofferDamInputProfile,
)
from koswat.dike_reinforcements.input_profile.cofferdam.cofferdam_input_profile_calculation import (
    CofferdamInputProfileCalculation,
)
from koswat.dike_reinforcements.input_profile.reinforcement_input_profile_calculation_protocol import (
    ReinforcementInputProfileCalculationProtocol,
)
from koswat.dike_reinforcements.reinforcement_profile.reinforcement_profile import (
    ReinforcementProfile,
)


class TestCofferdamInputProfileCalculation:
    def test_initialize(self):
        _calculation = CofferdamInputProfileCalculation()
        assert _calculation
        assert not _calculation.base_profile
        assert not _calculation.scenario
        assert isinstance(_calculation, CofferdamInputProfileCalculation)
        assert isinstance(_calculation, ReinforcementInputProfileCalculationProtocol)

    @pytest.mark.parametrize(
        "soil_polderside_berm_width, expected",
        [
            pytest.param(0.0, 13.5, id="soil_polderside_berm_width=0"),
            pytest.param(30.0, 14.5, id="soil_polderside_berm_width=30"),
        ],
    )
    def test__calculate_length_cofferdam(
        self, soil_polderside_berm_width: float, expected: float
    ):
        @dataclass
        class MockInputData(KoswatInputProfileProtocol):
            pleistocene: float
            aquifer: float

        @dataclass
        class MockSettings(KoswatCofferdamSettings):
            min_length_cofferdam: float
            max_length_cofferdam: float

        # 1. Define test data.
        _input_data = MockInputData(pleistocene=-5, aquifer=-2)
        _cofferdam_settings = MockSettings(
            min_length_cofferdam=0.0, max_length_cofferdam=99
        )
        _new_crest_height = 8.0

        # 2. Run test.
        _result = CofferdamInputProfileCalculation._calculate_length_cofferdam(
            _input_data,
            _cofferdam_settings,
            soil_polderside_berm_width,
            _new_crest_height,
        )

        # 3. Verify expectations
        assert _result == expected

    @pytest.mark.parametrize(
        "construction_length, expected",
        [
            pytest.param(10.0, ConstructionTypeEnum.KISTDAM, id="length > 0"),
            pytest.param(0.0, None, id="length = 0"),
        ],
    )
    def test__determine_construction_type(
        self, construction_length: float, expected: ConstructionTypeEnum | None
    ):
        # 1. Run test
        _result = CofferdamInputProfileCalculation._determine_construction_type(
            construction_length
        )

        # 2. Verify expectations
        assert _result == expected

    def test__calculate_new_waterside_slope(self):
        @dataclass
        class MockInputData(KoswatInputProfileProtocol):
            crest_height: float
            waterside_slope: float
            waterside_ground_level: float

        # 1. Define test data.
        _input_data = MockInputData(
            crest_height=8, waterside_ground_level=2, waterside_slope=3
        )
        _scenario = KoswatScenario(d_h=2)
        _expected_result = 2.25

        # 2. Run test.
        _result = CofferdamInputProfileCalculation._calculate_new_waterside_slope(
            _input_data, _scenario
        )

        # 3. Verify expectations
        assert _result == _expected_result

    def test_build(self, valid_input_data: KoswatInputProfileProtocol):
        @dataclass
        class MockSettings(KoswatCofferdamSettings):
            min_length_cofferdam: float
            max_length_cofferdam: float

        # 1. Define test data
        _calculator = CofferdamInputProfileCalculation()
        _calculator.base_profile = ReinforcementProfile(input_data=valid_input_data)
        _reinforcement_settings = KoswatReinforcementSettings(
            cofferdam_settings=MockSettings(
                min_length_cofferdam=0, max_length_cofferdam=99
            )
        )
        _calculator.reinforcement_settings = _reinforcement_settings
        _calculator.scenario = KoswatScenario(
            d_h=12.0, crest_width=6.7, waterside_slope=7.8
        )

        # 2. Run test.
        _result = _calculator.build()

        # 3. Verify expectations
        assert isinstance(_result, CofferDamInputProfile)
        assert isinstance(_result, KoswatInputProfileBase)
        assert isinstance(_result, KoswatInputProfileProtocol)

        assert _result.dike_section == "mocked_section"
        assert _result.waterside_ground_level == 6.7
        assert _result.waterside_slope == pytest.approx(6.534561)
        assert _result.waterside_berm_height == 19.8
        assert _result.waterside_berm_width == 8.9
        assert _result.crest_height == 42
        assert _result.crest_width == 6.7
        assert _result.polderside_slope == pytest.approx(3.139798)
        assert _result.polderside_berm_height == pytest.approx(10.182671)
        assert _result.polderside_berm_width == 9.0
        assert _result.polderside_ground_level == 2.3
        assert _result.ground_price_builtup == 150
        assert _result.ground_price_unbuilt == 10
        assert _result.factor_settlement == 1.2
        assert _result.pleistocene == -6.7
        assert _result.aquifer == -2.3
