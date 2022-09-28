import pytest
from shapely.geometry.point import Point

from koswat.profiles.koswat_input_profile import KoswatInputProfile
from koswat.profiles.koswat_profile import KoswatProfile
from koswat.profiles.polderside import Polderside
from koswat.profiles.waterside import Waterside
from tests.profiles.input_profile_cases import default_case


class TestKoswatProfile:
    def test_initialize_koswat_profile(self):
        _koswat_profile = KoswatProfile()
        assert _koswat_profile
        assert not _koswat_profile.input_data
        assert isinstance(_koswat_profile.waterside, Waterside)
        assert isinstance(_koswat_profile.polderside, Polderside)
        assert _koswat_profile.points == [None] * 8

    def test_given_koswat_default_input_profile(self):
        # 1. Define test data.
        assert isinstance(default_case, KoswatInputProfile)
        _expected_points = [
            Point(-18, 0),
            Point(-18, 0),
            Point(-18, 0),
            Point(0, 6),
            Point(5, 6),
            Point(23, 0),
            Point(23, 0),
            Point(23, 0),
        ]

        # 2. Run test.
        _koswat_profile = KoswatProfile.from_koswat_input_profile(default_case)

        # 3. Verify final expectations.
        assert _koswat_profile
        assert _koswat_profile.input_data == default_case
        assert isinstance(_koswat_profile.waterside, Waterside)
        assert isinstance(_koswat_profile.polderside, Polderside)
        assert _koswat_profile.points
        assert len(_koswat_profile.points) == 8
        assert _koswat_profile.points == _expected_points
