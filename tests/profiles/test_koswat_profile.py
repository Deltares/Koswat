from koswat.profiles.koswat_profile import KoswatProfileBase


class TestKoswatProfile:
    def test_initialize_koswat_profile(self):
        _koswat_profile = KoswatProfileBase()
        assert _koswat_profile
        assert not _koswat_profile.input_data
        assert not _koswat_profile.layers
        assert not _koswat_profile.characteristic_points
        assert _koswat_profile.points == []
