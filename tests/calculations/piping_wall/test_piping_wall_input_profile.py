from koswat.calculations.piping_wall.piping_wall_input_profile import (
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

    def test_from_dict(self):
        # 1. Define test data
        _test_data = dict(
            buiten_maaiveld=0.01,
            buiten_talud=0.02,
            buiten_berm_hoogte=0.03,
            buiten_berm_breedte=0.04,
            kruin_hoogte=0.05,
            kruin_breedte=0.06,
            binnen_talud=0.07,
            binnen_berm_hoogte=0.08,
            binnen_berm_breedte=0.09,
            binnen_maaiveld=0.10,
            length_stability_wall=0.11,
        )
        # 2. Run test
        _input = PipingWallInputProfile.from_dict(_test_data)

        # 3. Verify expectations.
        assert isinstance(_input, PipingWallInputProfile)
        assert isinstance(_input, KoswatInputProfileBase)
        assert isinstance(_input, KoswatInputProfileProtocol)
        assert _input.__dict__ == _test_data
