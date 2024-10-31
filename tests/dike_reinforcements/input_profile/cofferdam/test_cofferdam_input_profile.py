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

    def test_ground_price(self):
        # 1. Define test data
        _builtup = 100
        _unbuilt = 10
        _profile = CofferDamInputProfile()
        _profile.ground_price_builtup = _builtup
        _profile.ground_price_unbuilt = _unbuilt

        # 2. Run test
        _ground_price = _profile.ground_price

        # 3. Verify expectations
        assert _ground_price == _builtup
