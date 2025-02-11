from koswat.dike.koswat_input_profile_protocol import KoswatInputProfileProtocol
from koswat.dike.profile.koswat_input_profile_base import KoswatInputProfileBase
from koswat.dike_reinforcements.input_profile.reinforcement_input_profile_protocol import (
    ReinforcementInputProfileProtocol,
)
from koswat.dike_reinforcements.input_profile.soil.soil_input_profile import (
    SoilInputProfile,
)


class TestSoilInputProfile:
    def test_initialize(self):
        _input = SoilInputProfile()
        assert isinstance(_input, SoilInputProfile)
        assert isinstance(_input, KoswatInputProfileBase)
        assert isinstance(_input, KoswatInputProfileProtocol)
        assert isinstance(_input, ReinforcementInputProfileProtocol)

    def test_ground_price(self):
        # 1. Define test data
        _builtup = 100
        _unbuilt = 10
        _profile = SoilInputProfile()
        _profile.ground_price_builtup = _builtup
        _profile.ground_price_unbuilt = _unbuilt

        # 2. Run test
        _ground_price = _profile.ground_price

        # 3. Verify expectations
        assert _ground_price == _unbuilt
