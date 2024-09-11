from shapely.geometry import Point

from koswat.dike.surroundings.point.point_surroundings import PointSurroundings
from koswat.dike.surroundings.wrapper.surroundings_wrapper import (
    KoswatSurroundingsObstacle,
    SurroundingsWrapper,
)


class TestSurroundingsWrapper:
    def test_initialize(self):
        _surroundings = SurroundingsWrapper()
        assert isinstance(_surroundings, SurroundingsWrapper)
        assert not _surroundings.buildings_polderside
        assert not _surroundings.obstacle_locations

    def _to_surrounding_point(
        self, location: Point, distance: str
    ) -> PointSurroundings:
        _ps = PointSurroundings()
        _ps.location = location
        if distance:
            _ps.surroundings_matrix[distance] = 1
        return _ps

    def test_set_buildings_polderside(self):
        # 1. Define test data.
        _buildings_polderside = KoswatSurroundingsObstacle()
        _locations = [
            Point(4.2, 2.4),
            Point(4.2, 4.2),
            Point(2.4, 2.4),
        ]
        _buildings_polderside.points = list(
            map(self._to_surrounding_point, _locations, [[], [], []])
        )
        _surroundings = SurroundingsWrapper()
        assert isinstance(_surroundings, SurroundingsWrapper)

        # 2. Run test.
        _surroundings.buildings_polderside = _buildings_polderside

        # 3. Verify expectations.
        assert isinstance(
            _surroundings.buildings_polderside, KoswatSurroundingsObstacle
        )
        assert [x.location for x in _surroundings.obstacle_locations] == _locations

    def test_get_safe_locations(self):
        # 1. Define test data.
        _buildings_polderside = KoswatSurroundingsObstacle()
        _railways_polderside = KoswatSurroundingsObstacle()
        _waters_polderside = KoswatSurroundingsObstacle()
        _locations = [
            Point(4.2, 2.4),
            Point(4.2, 4.2),
            Point(2.4, 2.4),
        ]
        _distances = [
            [[], [20, 50], [10, 50]],
            [[], [15], [20]],
            [[5, 100], [5, 100], [5, 100]],
        ]
        _buildings_polderside.points = list(
            map(self._to_surrounding_point, _locations, _distances[0])
        )
        _railways_polderside.points = list(
            map(self._to_surrounding_point, _locations, _distances[1])
        )
        _waters_polderside.points = list(
            map(self._to_surrounding_point, _locations, _distances[2])
        )
        _surroundings = SurroundingsWrapper()
        assert isinstance(_surroundings, SurroundingsWrapper)

        # 2. Run test.
        _surroundings.buildings_polderside = _buildings_polderside
        _surroundings.railways_polderside = _railways_polderside
        _surroundings.waters_polderside = _waters_polderside
        _surroundings.apply_buildings = True
        _surroundings.apply_railways = True
        _surroundings.apply_waters = False
        _safe_points = _surroundings.get_locations_after_distance(12)

        # 3. Verify expectations.
        assert [x.location for x in _safe_points] == _locations[:2]
