from shapely import Point

from koswat.dike.characteristic_points.characteristic_points import CharacteristicPoints
from koswat.dike.koswat_profile_protocol import KoswatProfileProtocol
from koswat.dike.profile.koswat_profile import KoswatProfileBase


class TestKoswatProfile:
    def test_initialize_koswat_profile(self):
        _koswat_profile = KoswatProfileBase()
        assert isinstance(_koswat_profile, KoswatProfileBase)
        assert isinstance(_koswat_profile, KoswatProfileProtocol)
        assert _koswat_profile
        assert not _koswat_profile.input_data
        assert not _koswat_profile.layers_wrapper
        assert not _koswat_profile.characteristic_points
        assert not _koswat_profile.points

    def test_profile_height_returns_max_y_value(self):
        # 1. Define test data.
        _max_value = 100
        _base_profile = KoswatProfileBase(
            characteristic_points=CharacteristicPoints(
                p_1=Point(0, 4.2), p_2=Point(_max_value + 1, _max_value)
            )
        )

        # 2. Run test and verify expectations.
        assert _base_profile.profile_height == _max_value
