import pytest

from koswat.configuration.settings import KoswatScenario
from koswat.configuration.settings.reinforcements.koswat_vps_settings import (
    KoswatVPSSettings,
)
from koswat.core.protocols import BuilderProtocol
from koswat.dike.profile.koswat_input_profile_base import KoswatInputProfileBase
from koswat.dike_reinforcements.input_profile.reinforcement_input_profile_calculation_protocol import (
    ReinforcementInputProfileCalculationProtocol,
)
from koswat.dike_reinforcements.input_profile.soil.soil_input_profile_calculation import (
    SoilInputProfileCalculation,
)
from koswat.dike_reinforcements.input_profile.vertical_piping_solution.vps_input_profile_calculation import (
    VPSInputProfileCalculation,
)


class TestVPSInputProfileCalculation:
    def test_initialize(self):
        _calculation = VPSInputProfileCalculation()
        assert _calculation
        assert not _calculation.base_profile
        assert not _calculation.scenario
        assert isinstance(_calculation, VPSInputProfileCalculation)
        assert isinstance(_calculation, SoilInputProfileCalculation)
        assert isinstance(_calculation, ReinforcementInputProfileCalculationProtocol)
        assert isinstance(_calculation, BuilderProtocol)

    def test_calculate_new_input_profile(self):
        # 1. Define test data.
        _scenario = KoswatScenario()
        _scenario.d_h = 1
        _scenario.d_p = 30
        _scenario.crest_width = 5
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
        _vps_settings = KoswatVPSSettings()
        _vps_settings.polderside_berm_width_vps = 10

        # 2. Run test
        _new_profile = VPSInputProfileCalculation()._calculate_new_input_profile(
            _old_profile, _vps_settings, _scenario
        )

        # 3. Verify expectations
        assert (
            _new_profile.waterside_ground_level == _old_profile.waterside_ground_level
        )
        assert _new_profile.waterside_slope == _old_profile.waterside_slope
        assert _new_profile.waterside_berm_height == _old_profile.waterside_berm_height
        assert _new_profile.waterside_berm_width == _old_profile.waterside_berm_width
        assert _new_profile.crest_height == pytest.approx(7, 0.0001)
        assert _new_profile.crest_width == _scenario.crest_width
        assert _new_profile.polderside_slope == pytest.approx(3, 0.0001)
        assert (
            _new_profile.polderside_ground_level == _old_profile.polderside_ground_level
        )
        assert _new_profile.polderside_berm_width == pytest.approx(10, 0.0001)
        assert _new_profile.polderside_berm_height == pytest.approx(0.5, 0.0001)
