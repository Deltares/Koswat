from koswat.dike_reinforcements.reinforcement_input_profiles.stability_wall.stability_wall_input_profile import (
    StabilityWallInputProfile,
)
from koswat.dike.koswat_input_profile_protocol import KoswatInputProfileProtocol
from koswat.dike.profile.koswat_input_profile_base import KoswatInputProfileBase


class TestStabilityWallInputProfile:
    def test_initialize(self):
        _input = StabilityWallInputProfile()
        assert isinstance(_input, StabilityWallInputProfile)
        assert isinstance(_input, KoswatInputProfileBase)
        assert isinstance(_input, KoswatInputProfileProtocol)
