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
        _scenario.polderside_slope = 3
        _old_profile = KoswatInputProfileBase()
        _old_profile.buiten_maaiveld = 0
        _old_profile.buiten_talud = 3
        _old_profile.buiten_berm_hoogte = 0
        _old_profile.buiten_berm_breedte = 0
        _old_profile.kruin_hoogte = 6
        _old_profile.kruin_breedte = 5
        _old_profile.binnen_talud = 3
        _old_profile.binnen_berm_hoogte = 0
        _old_profile.binnen_berm_breedte = 0
        _old_profile.binnen_maaiveld = 0
        _vps_settings = KoswatVPSSettings()
        _vps_settings.polderside_berm_width_vps = 10

        # 2. Run test
        _new_profile = VPSInputProfileCalculation()._calculate_new_input_profile(
            _old_profile, _vps_settings, _scenario
        )

        # 3. Verify expectations
        assert _new_profile.buiten_maaiveld == _old_profile.buiten_maaiveld
        assert _new_profile.buiten_talud == _old_profile.buiten_talud
        assert _new_profile.buiten_berm_hoogte == _old_profile.buiten_berm_hoogte
        assert _new_profile.buiten_berm_breedte == _old_profile.buiten_berm_breedte
        assert _new_profile.kruin_hoogte == pytest.approx(7, 0.0001)
        assert _new_profile.kruin_breedte == _scenario.crest_width
        assert _new_profile.binnen_talud == pytest.approx(3, 0.0001)
        assert _new_profile.binnen_maaiveld == _old_profile.binnen_maaiveld
        assert _new_profile.binnen_berm_breedte == pytest.approx(10, 0.0001)
        assert _new_profile.binnen_berm_hoogte == pytest.approx(0.5, 0.0001)
