from koswat.dike.koswat_input_profile_protocol import KoswatInputProfileProtocol
from koswat.dike.profile.koswat_input_profile_base import KoswatInputProfileBase
from koswat.dike_reinforcements.input_profile.piping_wall.piping_wall_input_profile import (
    PipingWallInputProfile,
)


class TestPipingWallInputProfile:
    def test_initialize(self):
        _input = PipingWallInputProfile()
        assert isinstance(_input, PipingWallInputProfile)
        assert isinstance(_input, KoswatInputProfileBase)
        assert isinstance(_input, KoswatInputProfileProtocol)
