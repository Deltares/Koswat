from koswat.profiles.koswat_profile import KoswatProfile
from koswat.profiles.polderside import Polderside
from koswat.profiles.waterside import Waterside


class TestKoswatProfile:
    def test_initialize_koswat_profile(self):
        _koswat_profile = KoswatProfile()
        assert _koswat_profile
        assert not _koswat_profile.input_data
        assert not _koswat_profile.layers
        assert isinstance(_koswat_profile.waterside, Waterside)
        assert isinstance(_koswat_profile.polderside, Polderside)
        assert _koswat_profile.points == [None] * 8
