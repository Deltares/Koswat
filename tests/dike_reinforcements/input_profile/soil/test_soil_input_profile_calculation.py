import pytest

from koswat.configuration.settings import KoswatScenario
from koswat.configuration.settings.reinforcements.koswat_soil_settings import (
    KoswatSoilSettings,
)
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

    def test_calculate_new_binnen_talud(self):
        # 1. Define test data.
        _expected_value = 3.57
        _scenario = KoswatScenario()
        _scenario.d_h = 1
        _scenario.d_s = 10
        _scenario.d_p = 30
        _scenario.kruin_breedte = 5
        _scenario.buiten_talud = 3
        _input_profile = KoswatInputProfileBase()
        _input_profile.crest_width = 5
        _input_profile.crest_height = 8
        _input_profile.polderside_slope = 3
        _input_profile.polderside_ground_level = 2

        # 2. Run test
        _new_binnen_talud = SoilInputProfileCalculation()._calculate_new_binnen_talud(
            _input_profile, _scenario
        )

        # 3. Verify expectations
        assert _new_binnen_talud == pytest.approx(_expected_value, 0.001)

    def test_calculate_new_binnen_berm_hoogte_positive_binnen_berm_breedte(self):
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
        _new_binnen_berm_hoogte = (
            SoilInputProfileCalculation()._calculate_new_binnen_berm_hoogte(
                _old_data, _new_data, _scenario
            )
        )

        # 3. Verify expectations
        assert _new_binnen_berm_hoogte == pytest.approx(_expected_value, 0.001)

    def test_calculate_new_binnen_berm_hoogte_negative_binnen_berm_breedte(self):
        # 1. Define test data.
        _scenario = KoswatScenario()
        _old_data = KoswatInputProfileBase()
        _old_data.polderside_ground_level = 4.2

        _new_data = KoswatInputProfileBase()
        _new_data.polderside_berm_width = -1

        # 2. Run test
        _new_binnen_berm_hoogte = (
            SoilInputProfileCalculation()._calculate_new_binnen_berm_hoogte(
                _old_data, _new_data, _scenario
            )
        )

        # 3. Verify expectations
        assert _new_binnen_berm_hoogte == _old_data.polderside_ground_level

    def test_calculate_new_binnen_berm_breedte(self):
        # 1. Define test data.
        _expected_value = 20
        _scenario = KoswatScenario()
        _scenario.d_h = 1
        _scenario.d_p = 30
        _scenario.buiten_talud = 3
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
        _new_binnen_berm_breedte = (
            SoilInputProfileCalculation()._calculate_soil_binnen_berm_breedte(
                _old_profile, _new_profile, _scenario
            )
        )

        # 3. Verify expectations
        assert _new_binnen_berm_breedte == pytest.approx(_expected_value, 0.001)

    def test_calculate_new_kruin_hoogte(self):
        # 1. Define test data.
        _expected_value = 42.24
        _scenario = KoswatScenario()
        _scenario.d_h = 2.2
        _old_data = KoswatInputProfileBase()
        _old_data.crest_height = 40.04

        # 2. Run test
        _new_kruin_hoogte = SoilInputProfileCalculation()._calculate_new_kruin_hoogte(
            _old_data, _scenario
        )

        # 3. Verify expectations
        assert _new_kruin_hoogte == pytest.approx(_expected_value, 0.001)
