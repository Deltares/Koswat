from koswat.calculations.protocols import ReinforcementProfileProtocol
from koswat.calculations.standard_reinforcement.piping_wall.piping_wall_reinforcement_profile import (
    PipingWallReinforcementProfile,
)
from koswat.calculations.standard_reinforcement.standard_reinforcement_profile import (
    StandardReinforcementProfile,
)
from koswat.dike.koswat_profile_protocol import KoswatProfileProtocol
from koswat.dike.profile.koswat_profile import KoswatProfileBase


class TestPipingWallReinforcementProfile:
    def test_initialize(self):
        _profile = PipingWallReinforcementProfile()
        assert isinstance(_profile, PipingWallReinforcementProfile)
        assert isinstance(_profile, StandardReinforcementProfile)
        assert isinstance(_profile, ReinforcementProfileProtocol)
        assert isinstance(_profile, KoswatProfileProtocol)
        assert isinstance(_profile, KoswatProfileBase)
        assert str(_profile) == "Kwelscherm"
