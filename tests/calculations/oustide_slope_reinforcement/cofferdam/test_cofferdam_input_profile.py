from koswat.dike_reinforcements.reinforcement_input_profiles.reinforcement_input_profile_protocol import (
    ReinforcementInputProfileProtocol,
)
from koswat.dike_reinforcements.reinforcement_input_profiles.cofferdam.cofferdam_input_profile import (
    CofferDamInputProfile,
)
from koswat.dike.koswat_input_profile_protocol import KoswatInputProfileProtocol
from koswat.dike.profile.koswat_input_profile_base import KoswatInputProfileBase


class TestCofferDamInputProfile:
    def test_initialize(self):
        _input = CofferDamInputProfile()
        assert isinstance(_input, CofferDamInputProfile)
        assert isinstance(_input, KoswatInputProfileBase)
        assert isinstance(_input, KoswatInputProfileProtocol)
        assert isinstance(_input, ReinforcementInputProfileProtocol)
