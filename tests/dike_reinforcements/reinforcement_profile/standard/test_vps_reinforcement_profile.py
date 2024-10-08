from koswat.dike.koswat_profile_protocol import KoswatProfileProtocol
from koswat.dike.profile.koswat_profile import KoswatProfileBase
from koswat.dike_reinforcements.reinforcement_profile.reinforcement_profile_protocol import (
    ReinforcementProfileProtocol,
)
from koswat.dike_reinforcements.reinforcement_profile.standard.standard_reinforcement_profile import (
    StandardReinforcementProfile,
)
from koswat.dike_reinforcements.reinforcement_profile.standard.vps_reinforcement_profile import (
    VPSReinforcementProfile,
)


class TestVPSReinforcementProfile:
    def test_initialize(self):
        _profile = VPSReinforcementProfile()
        assert isinstance(_profile, VPSReinforcementProfile)
        assert isinstance(_profile, StandardReinforcementProfile)
        assert isinstance(_profile, ReinforcementProfileProtocol)
        assert isinstance(_profile, KoswatProfileProtocol)
        assert isinstance(_profile, KoswatProfileBase)
