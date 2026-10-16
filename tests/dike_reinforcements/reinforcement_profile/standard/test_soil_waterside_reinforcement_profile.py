import pytest

from koswat.dike.koswat_profile_protocol import KoswatProfileProtocol
from koswat.dike.profile.koswat_profile import KoswatProfileBase
from koswat.dike_reinforcements.input_profile.soil_waterside.soil_waterside_input_profile import (
    SoilWatersideInputProfile,
)
from koswat.dike_reinforcements.reinforcement_profile.reinforcement_profile_protocol import (
    ReinforcementProfileProtocol,
)
from koswat.dike_reinforcements.reinforcement_profile.standard import (
    SoilWatersideReinforcementProfile,
)
from koswat.dike_reinforcements.reinforcement_profile.standard.standard_reinforcement_profile import (
    StandardReinforcementProfile,
)


class TestSoilWatersideReinforcementProfile:
    def test_initialize(self):
        _profile = SoilWatersideReinforcementProfile()
        assert isinstance(_profile, SoilWatersideReinforcementProfile)
        assert isinstance(_profile, StandardReinforcementProfile)
        assert isinstance(_profile, ReinforcementProfileProtocol)
        assert isinstance(_profile, KoswatProfileProtocol)
        assert isinstance(_profile, KoswatProfileBase)

    @pytest.mark.parametrize(
        "waterside_slope, waterside_berm_height, waterside_berm_width, expected_value",
        [
            pytest.param(1.0, 2.0, 5.0, False, id="No change"),
            pytest.param(2.0, 2.0, 5.0, True, id="Slope changed"),
            pytest.param(1.0, 3.0, 5.0, True, id="Berm height changed"),
            pytest.param(1.0, 2.0, 6.0, True, id="Berm width changed"),
            pytest.param(2.0, 3.0, 6.0, True, id="All changed"),
        ],
    )
    def test_when_waterside_changed_given_profile_returns_expected(
        self,
        waterside_slope: float,
        waterside_berm_height: float,
        waterside_berm_width: float,
        expected_value: bool,
    ):
        # 1. Define test data
        _profile = SoilWatersideReinforcementProfile()
        _profile.input_data = SoilWatersideInputProfile(
            waterside_slope=waterside_slope,
            waterside_berm_height=waterside_berm_height,
            waterside_berm_width=waterside_berm_width,
        )
        _profile.old_profile = KoswatProfileBase()
        _profile.old_profile.input_data = SoilWatersideInputProfile(
            waterside_slope=1.0,
            waterside_berm_height=2.0,
            waterside_berm_width=5.0,
        )

        # 2. Run test
        _result = _profile.waterside_changed

        # 3. Verify result
        assert _result is expected_value
