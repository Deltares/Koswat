from koswat.calculations.cofferdam.cofferdam_reinforcement_profile import (
    CofferdamReinforcementProfile,
)
from koswat.calculations.outside_slope_reinforcement_profile_protocol import (
    OutsideSlopeReinforcementProfileProtocol,
)
from koswat.calculations.reinforcement_profile_protocol import (
    ReinforcementProfileProtocol,
)
from koswat.dike.koswat_profile_protocol import KoswatProfileProtocol
from koswat.dike.profile.koswat_profile import KoswatProfileBase


class TestCofferDamReinforcementProfile:
    def test_initialize(self):
        _profile = CofferdamReinforcementProfile()
        assert isinstance(_profile, CofferdamReinforcementProfile)
        assert isinstance(_profile, OutsideSlopeReinforcementProfileProtocol)
        assert isinstance(_profile, ReinforcementProfileProtocol)
        assert isinstance(_profile, KoswatProfileProtocol)
        assert isinstance(_profile, KoswatProfileBase)
        assert str(_profile) == "Kistdam"
