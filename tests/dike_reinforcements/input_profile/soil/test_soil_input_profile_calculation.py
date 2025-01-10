from dataclasses import dataclass

import pytest

from koswat.configuration.settings import KoswatScenario
from koswat.configuration.settings.reinforcements.koswat_reinforcement_settings import (
    KoswatReinforcementSettings,
)
from koswat.configuration.settings.reinforcements.koswat_soil_settings import (
    KoswatSoilSettings,
)
from koswat.core.protocols import BuilderProtocol
from koswat.dike.koswat_input_profile_protocol import KoswatInputProfileProtocol
from koswat.dike.profile.koswat_input_profile_base import KoswatInputProfileBase
from koswat.dike_reinforcements.input_profile.reinforcement_input_profile_calculation_protocol import (
    ReinforcementInputProfileCalculationProtocol,
)
from koswat.dike_reinforcements.input_profile.soil.soil_input_profile import (
    SoilInputProfile,
)
from koswat.dike_reinforcements.input_profile.soil.soil_input_profile_calculation import (
    SoilInputProfileCalculation,
)
from koswat.dike_reinforcements.reinforcement_profile.reinforcement_profile import (
    ReinforcementProfile,
)


class TestSoilInputProfileCalculation:
    def test_initialize(self):
        _calculation = SoilInputProfileCalculation()
        assert _calculation
        assert not _calculation.base_profile
        assert not _calculation.scenario
        assert isinstance(_calculation, SoilInputProfileCalculation)
        assert isinstance(_calculation, ReinforcementInputProfileCalculationProtocol)
        assert isinstance(_calculation, BuilderProtocol)

    def test_build(self, valid_input_data: KoswatInputProfileProtocol):
        @dataclass
        class MockSettings(KoswatSoilSettings):
            min_berm_height: float
            max_berm_height_factor: float
            factor_increase_berm_height: float

        # 1. Define test data.
        _calculator = SoilInputProfileCalculation()
        _calculator.base_profile = ReinforcementProfile(input_data=valid_input_data)
        _reinforcement_settings = KoswatReinforcementSettings(
            soil_settings=MockSettings(
                min_berm_height=1.0,
                max_berm_height_factor=0.1,
                factor_increase_berm_height=0.2,
            )
        )
        _calculator.reinforcement_settings = _reinforcement_settings
        _calculator.scenario = KoswatScenario(
            d_h=12.0, crest_width=6.7, waterside_slope=7.8
        )

        # 2. Run test.
        _result = _calculator.build()

        # 3. Verify Expectations.
        assert isinstance(_result, SoilInputProfile)
        assert isinstance(_result, KoswatInputProfileBase)
        assert isinstance(_result, KoswatInputProfileProtocol)

        assert _result.dike_section == "mocked_section"
        assert _result.waterside_ground_level == 6.7
        assert _result.waterside_slope == 7.8
        assert _result.waterside_berm_height == 19.8
        assert _result.waterside_berm_width == 8.9
        assert _result.crest_height == 42.0
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
