import math
from typing import Callable

from shapely.geometry import Point

from koswat.dike.surroundings.surroundings_polderside.koswat_surroundings_polderside import (
    KoswatSurroundingsPolderside,
    PointSurroundings,
)


class TestKoswatSurroundingsPolderside:
    def test_initialize_koswat_buildings_polderside(self):
        _ksp = KoswatSurroundingsPolderside()
        assert isinstance(_ksp, KoswatSurroundingsPolderside)
        assert not _ksp.conflicting_points
        assert not _ksp.get_classify_surroundings()

    def test_classify_surroundings(
        self,
        surroundings_point_builder: Callable[[Point, list[float]], PointSurroundings],
    ):
        # 1. Define test data
        _first_point = Point(2.4, 4.2)
        _second_point = Point(4.2, 4.2)
        _third_point = Point(4.2, 2.4)
        _fourth_point = Point(2.4, 2.4)
        _surrounding_points = [
            surroundings_point_builder(_first_point, [2, 4]),
            surroundings_point_builder(_second_point, [4]),
            surroundings_point_builder(_third_point, [2]),
            surroundings_point_builder(_fourth_point, []),
        ]

        # 2. Run test
        _ksp = KoswatSurroundingsPolderside()
        _ksp.points = _surrounding_points
        _classified_surroundings = _ksp.get_classify_surroundings()

        # 3. Verify expectations.
        assert isinstance(_classified_surroundings, dict)
        assert all(csk in [math.nan, 2, 4] for csk in _classified_surroundings.keys())
        assert _classified_surroundings[math.nan] == [_fourth_point]
        assert _classified_surroundings[2] == [_first_point, _third_point]
        assert _classified_surroundings[4] == [_second_point]
