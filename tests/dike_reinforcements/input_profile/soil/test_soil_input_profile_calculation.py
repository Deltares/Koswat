import pytest

from koswat.configuration.settings import KoswatScenario
from koswat.core.protocols import BuilderProtocol
from koswat.dike.profile.koswat_input_profile_base import KoswatInputProfileBase
from koswat.dike_reinforcements.input_profile.reinforcement_input_profile_calculation_protocol import (
    ReinforcementInputProfileCalculationProtocol,
)
from koswat.dike_reinforcements.input_profile.soil.soil_input_profile_calculation import (
    SoilInputProfileCalculation,
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

    def test_calculate_new_polderside_slope(self):
        # 1. Define test data.
        _expected_value = 3.57
        _scenario = KoswatScenario()
        _scenario.d_h = 1
        _scenario.d_s = 10
        _scenario.d_p = 30
        _scenario.crest_width = 5
        _scenario.waterside_slope = 3
        _input_profile = KoswatInputProfileBase()
        _input_profile.crest_width = 5
        _input_profile.crest_height = 8
        _input_profile.polderside_slope = 3
        _input_profile.polderside_ground_level = 2

        # 2. Run test
        _new_polderside_slope = (
            SoilInputProfileCalculation()._calculate_new_polderside_slope(
                _input_profile, _scenario
            )
        )

        # 3. Verify expectations
        assert _new_polderside_slope == pytest.approx(_expected_value, 0.001)

    def test_calculate_new_polderside_berm_height_positive_polderside_berm_width(self):
        # 1. Define test data.
        _expected_value = 3.0
        _scenario = KoswatScenario()
        _scenario.d_h = 1
        _old_data = KoswatInputProfileBase()
        _old_data.polderside_berm_height = 2
        _old_data.polderside_ground_level = 2
        _old_data.crest_height = 8
        _new_data = KoswatInputProfileBase()
        _new_data.polderside_berm_width = 20

        # 2. Run test
        _new_polderside_berm_height = (
            SoilInputProfileCalculation()._calculate_new_polderside_berm_height(
                _old_data, _new_data, _scenario
            )
        )

        # 3. Verify expectations
        assert _new_polderside_berm_height == pytest.approx(_expected_value, 0.001)

    def test_calculate_new_polderside_berm_height_negative_polderside_berm_width(self):
        # 1. Define test data.
        _scenario = KoswatScenario()
        _old_data = KoswatInputProfileBase()
        _old_data.polderside_ground_level = 4.2

        _new_data = KoswatInputProfileBase()
        _new_data.polderside_berm_width = -1

        # 2. Run test
        _new_polderside_berm_height = (
            SoilInputProfileCalculation()._calculate_new_polderside_berm_height(
                _old_data, _new_data, _scenario
            )
        )

        # 3. Verify expectations
        assert _new_polderside_berm_height == _old_data.polderside_ground_level

    def test_calculate_new_polderside_berm_width(self):
        # 1. Define test data.
        _expected_value = 20
        _scenario = KoswatScenario()
        _scenario.d_h = 1
        _scenario.d_p = 30
        _scenario.waterside_slope = 3
        _old_profile = KoswatInputProfileBase()
        _old_profile.waterside_ground_level = 0
        _old_profile.waterside_slope = 3
        _old_profile.waterside_berm_height = 0
        _old_profile.waterside_berm_width = 0
        _old_profile.crest_height = 6
        _old_profile.crest_width = 5
        _old_profile.polderside_slope = 3
        _old_profile.polderside_berm_height = 0
        _old_profile.polderside_berm_width = 0
        _old_profile.polderside_ground_level = 0
        _new_profile = KoswatInputProfileBase()
        _new_profile.waterside_ground_level = 0
        _new_profile.waterside_slope = 3
        _new_profile.waterside_berm_width = 0
        _new_profile.crest_width = 5
        _new_profile.crest_height = 7
        _new_profile.polderside_slope = 3.5714
        _new_profile.polderside_ground_level = 0

        # 2. Run test
        _new_polderside_berm_width = (
            SoilInputProfileCalculation()._calculate_soil_polderside_berm_width(
                _old_profile, _new_profile, _scenario
            )
        )

        # 3. Verify expectations
        assert _new_polderside_berm_width == pytest.approx(_expected_value, 0.001)

    def test_calculate_new_crest_height(self):
        # 1. Define test data.
        _expected_value = 42.24
        _scenario = KoswatScenario()
        _scenario.d_h = 2.2
        _old_data = KoswatInputProfileBase()
        _old_data.crest_height = 40.04

        # 2. Run test
        _new_crest_height = SoilInputProfileCalculation()._calculate_new_crest_height(
            _old_data, _scenario
        )

        # 3. Verify expectations
        assert _new_crest_height == pytest.approx(_expected_value, 0.001)
