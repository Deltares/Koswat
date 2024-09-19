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

    def test_grondprijs(self):
        # 1. Define test data
        _bebouwd = 100
        _onbebouwd = 10
        _profile = SoilInputProfile()
        _profile.grondprijs_bebouwd = _bebouwd
        _profile.grondprijs_onbebouwd = _onbebouwd

        # 2. Run test
        _grondprijs = _profile.grondprijs

        # 3. Verify expectations
        assert _grondprijs == _onbebouwd