from shapely.geometry.point import Point

from koswat.profiles.koswat_input_profile import KoswatInputProfile
from koswat.profiles.polderside import Polderside
from koswat.profiles.side_protocol import SideProtocol
from tests.profiles.input_profile_cases import default_case


class TestPolderside:
    def test_instance_polderside(self):
        _polderside = Polderside()
        assert isinstance(_polderside, Polderside)
        assert isinstance(_polderside, SideProtocol)
        assert _polderside.points == [None] * 4

    def test_from_input_profile_default_gets_polderside(self):
        # 1. Define test data
        _expected_points = [
            Point(5, 6),
            Point(23, 0),
            Point(23, 0),
            Point(23, 0),
        ]
        assert isinstance(default_case, KoswatInputProfile)

        # 2. Run test.
        _polderside = Polderside.from_input_profile(default_case)

        # 3. Verify final expectations
        assert isinstance(_polderside, Polderside)
        assert isinstance(_polderside, SideProtocol)
        assert _polderside.p_5 == _expected_points[0]
        assert _polderside.p_6 == _expected_points[1]
        assert _polderside.p_7 == _expected_points[2]
        assert _polderside.p_8 == _expected_points[3]
        assert _polderside.points == _expected_points
