import pytest
from shapely.geometry import Point

from koswat.dike_reinforcements.reinforcement_profile.outside_slope.outside_slope_reinforcement_profile import (
    OutsideSlopeReinforcementProfile,
)
from koswat.dike_reinforcements.reinforcement_profile.reinforcement_profile_protocol import (
    ReinforcementProfileProtocol,
)
from koswat.dike.characteristic_points.characteristic_points import CharacteristicPoints
from koswat.dike.profile.koswat_profile import KoswatProfileBase


class TestOutsideSlopeReinforcementProfile:
    def test_initialize(self):
        _reinforcement = OutsideSlopeReinforcementProfile()
        assert isinstance(_reinforcement, OutsideSlopeReinforcementProfile)
        assert isinstance(_reinforcement, ReinforcementProfileProtocol)
        assert isinstance(_reinforcement, KoswatProfileBase)

    def test_get_new_ground_level_surface(self):
        # 1. Define test data.
        _reinforcement = OutsideSlopeReinforcementProfile()
        _reinforcement.characteristic_points = CharacteristicPoints()
        _reinforcement.characteristic_points.p_1 = Point(0, 0)
        _reinforcement.characteristic_points.p_8 = Point(4.4, 0)
        assert _reinforcement.profile_width == 4.4
        _reinforcement.old_profile = OutsideSlopeReinforcementProfile()
        _reinforcement.old_profile.characteristic_points = CharacteristicPoints()
        _reinforcement.old_profile.characteristic_points.p_1 = Point(0, 0)
        _reinforcement.old_profile.characteristic_points.p_8 = Point(2.4, 0)
        assert _reinforcement.old_profile.profile_width == 2.4

        # 2.  Verify expectations
        assert _reinforcement.new_ground_level_surface == pytest.approx(2.0, 0.001)
