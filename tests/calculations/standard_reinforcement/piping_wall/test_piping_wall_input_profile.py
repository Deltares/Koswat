from koswat.dike_reinforcements.reinforcement_input_profiles.piping_wall.piping_wall_input_profile import (
    PipingWallInputProfile,
)
from koswat.dike.koswat_input_profile_protocol import KoswatInputProfileProtocol
from koswat.dike.profile.koswat_input_profile_base import KoswatInputProfileBase


class TestPipingWallInputProfile:
    def test_initialize(self):
        _input = PipingWallInputProfile()
        assert isinstance(_input, PipingWallInputProfile)
        assert isinstance(_input, KoswatInputProfileBase)
        assert isinstance(_input, KoswatInputProfileProtocol)
