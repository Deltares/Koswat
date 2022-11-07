from koswat.calculations.reinforcement_profile_protocol import (
    ReinforcementProfileProtocol,
)
from koswat.calculations.soil.soil_reinforcement_profile import SoilReinforcementProfile
from koswat.calculations.standard_reinforcement_profile_protocol import (
    StandardReinforcementProfile,
)
from koswat.dike.koswat_profile_protocol import KoswatProfileProtocol
from koswat.dike.profile.koswat_profile import KoswatProfileBase


class TestSoilReinforcementProfile:
    def test_initialize(self):
        _profile = SoilReinforcementProfile()
        assert isinstance(_profile, SoilReinforcementProfile)
        assert isinstance(_profile, StandardReinforcementProfile)
        assert isinstance(_profile, ReinforcementProfileProtocol)
        assert isinstance(_profile, KoswatProfileProtocol)
        assert isinstance(_profile, KoswatProfileBase)
        assert str(_profile) == "Grondmaatregel profiel"
