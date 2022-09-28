from shapely.geometry.point import Point

from koswat.profiles.koswat_input_profile import KoswatInputProfile
from koswat.profiles.side_protocol import SideProtocol
from koswat.profiles.waterside import Waterside
from tests.profiles.input_profile_cases import default_case


class TestWaterside:
    def test_instance_waterside(self):
        _waterside = Waterside()
        assert isinstance(_waterside, Waterside)
        assert isinstance(_waterside, SideProtocol)
        assert _waterside.points == [None] * 4

    def test_from_input_profile_default_gets_waterside(self):
        # 1. Define test data
        _expected_points = [
            Point(-18, 0),
            Point(-18, 0),
            Point(-18, 0),
            Point(0, 6),
        ]
        assert isinstance(default_case, KoswatInputProfile)

        # 2. Run test.
        _waterside = Waterside.from_input_profile(default_case)

        # 3. Verify final expectations
        assert isinstance(_waterside, Waterside)
        assert isinstance(_waterside, SideProtocol)
        assert _waterside.p_1 == _expected_points[0]
        assert _waterside.p_2 == _expected_points[1]
        assert _waterside.p_3 == _expected_points[2]
        assert _waterside.p_4 == _expected_points[3]
        assert _waterside.points == _expected_points
