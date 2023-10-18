import math
from typing import List

from shapely.geometry import Point

from koswat.dike.surroundings.buildings_polderside.koswat_buildings_polderside import (
    KoswatBuildingsPolderside,
    PointSurroundings,
)


class TestKoswatBuildingsPolderside:
    def _to_surrounding_point(
        self, location: Point, distance_list: List[float]
    ) -> PointSurroundings:
        _ps = PointSurroundings()
        _ps.location = location
        _ps.distance_to_surroundings = distance_list
        return _ps

    def test_initialize_koswat_buildings_polderside(self):
        _kbp = KoswatBuildingsPolderside()
        assert isinstance(_kbp, KoswatBuildingsPolderside)
        assert not _kbp.conflicting_points
        assert not _kbp.get_classify_surroundings()

    def test_classify_surroundings(self):
        # 1. Define test data
        _first_point = Point(2.4, 4.2)
        _second_point = Point(4.2, 4.2)
        _third_point = Point(4.2, 2.4)
        _fourth_point = Point(2.4, 2.4)
        _surrounding_points = [
            self._to_surrounding_point(_first_point, [2, 4]),
            self._to_surrounding_point(_second_point, [4]),
            self._to_surrounding_point(_third_point, [2]),
            self._to_surrounding_point(_fourth_point, []),
        ]

        # 2. Run test
        _kbp = KoswatBuildingsPolderside()
        _kbp.points = _surrounding_points
        _classified_surroundings = _kbp.get_classify_surroundings()

        # 3. Verify expectations.
        assert isinstance(_classified_surroundings, dict)
        assert all(csk in [math.nan, 2, 4] for csk in _classified_surroundings.keys())
        assert _classified_surroundings[math.nan] == [_fourth_point]
        assert _classified_surroundings[2] == [_first_point, _third_point]
        assert _classified_surroundings[4] == [_second_point]
