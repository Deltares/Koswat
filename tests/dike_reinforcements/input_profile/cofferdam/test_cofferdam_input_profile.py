from koswat.dike.koswat_input_profile_protocol import KoswatInputProfileProtocol
from koswat.dike.profile.koswat_input_profile_base import KoswatInputProfileBase
from koswat.dike_reinforcements.input_profile.cofferdam.cofferdam_input_profile import (
    CofferDamInputProfile,
)
from koswat.dike_reinforcements.input_profile.reinforcement_input_profile_protocol import (
    ReinforcementInputProfileProtocol,
)


class TestCofferDamInputProfile:
    def test_initialize(self):
        _input = CofferDamInputProfile()
        assert isinstance(_input, CofferDamInputProfile)
        assert isinstance(_input, KoswatInputProfileBase)
        assert isinstance(_input, KoswatInputProfileProtocol)
        assert isinstance(_input, ReinforcementInputProfileProtocol)

    def test_grondprijs(self):
        # 1. Define test data
        _bebouwd = 100
        _onbebouwd = 10
        _profile = CofferDamInputProfile()
        _profile.grondprijs_bebouwd = _bebouwd
        _profile.grondprijs_onbebouwd = _onbebouwd

        # 2. Run test
        _grondprijs = _profile.grondprijs

        # 3. Verify expectations
        assert _grondprijs == _bebouwd
