from koswat.dike_reinforcements.reinforcement_profiles.outside_slope_reinforcement.cofferdam.cofferdam_input_profile import (
    CofferDamInputProfile,
)
from koswat.dike_reinforcements.reinforcement_profiles.reinforcement_profile_protocol import (
    ReinforcementProfileProtocol,
)
from koswat.dike.koswat_input_profile_protocol import KoswatInputProfileProtocol
from koswat.dike.profile.koswat_input_profile_base import KoswatInputProfileBase


class TestCofferDamInputProfile:
    def test_initialize(self):
        _input = CofferDamInputProfile()
        assert isinstance(_input, CofferDamInputProfile)
        assert isinstance(_input, KoswatInputProfileBase)
        assert isinstance(_input, KoswatInputProfileProtocol)
        assert isinstance(_input, ReinforcementProfileProtocol)
