from typing import List

import pytest
from shapely.geometry.point import Point

from koswat.calculations.koswat_profile_reinforcement_cost_builder import (
    ProfileReinforcementCostBuilder,
)
from koswat.profiles.koswat_profile import KoswatProfile


class TestProfileVolumeCalculator:
    def _get_koswat_profile_from_points(self, points: List[Point]) -> KoswatProfile:
        _new_profile = KoswatProfile()
        _new_profile.waterside.p_1 = points[0]
        _new_profile.waterside.p_2 = points[2]
        _new_profile.waterside.p_3 = points[2]
        _new_profile.waterside.p_4 = points[3]
        _new_profile.polderside.p_5 = points[4]
        _new_profile.polderside.p_6 = points[5]
        _new_profile.polderside.p_7 = points[6]
        _new_profile.polderside.p_8 = points[7]
        return _new_profile

    @pytest.mark.skip(reason="Work in progress.")
    def test_profile_volume_calculator(self):
        _old_profile = self._get_koswat_profile_from_points(
            [
                Point(-18, 0),
                Point(-18, 0),
                Point(-18, 0),
                Point(0, 6),
                Point(5, 6),
                Point(23, 0),
                Point(23, 0),
                Point(23, 0),
            ]
        )
        _new_profile = self._get_koswat_profile_from_points(
            [
                Point(-21.0, 0.0),
                Point(-21.0, 0.0),
                Point(-21.0, 0.0),
                Point(0.0, 7.0),
                Point(5.0, 7.0),
                Point(26.42, 1.0),
                Point(46.42, 1.0),
                Point(49.99, 0.0),
            ]
        )
        assert isinstance(_new_profile, KoswatProfile)
        assert isinstance(_old_profile, KoswatProfile)

        # 2. Run test
        _total_volume = ProfileReinforcementCostBuilder().calculate_total_volume(
            _old_profile, _new_profile
        )

        # 3. Verify final expectations
        assert _total_volume > 0
