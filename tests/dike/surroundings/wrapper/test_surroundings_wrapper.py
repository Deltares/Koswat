from shapely.geometry import Point

from koswat.dike.surroundings.surroundings_polderside.koswat_surroundings_polderside import (
    KoswatSurroundingsPolderside,
    PointSurroundings,
)
from koswat.dike.surroundings.wrapper.surroundings_wrapper import SurroundingsWrapper


class TestSurroundingsWrapper:
    def test_initialize(self):
        _surroundings = SurroundingsWrapper()
        assert isinstance(_surroundings, SurroundingsWrapper)
        assert not _surroundings.buildings_polderside
        assert not _surroundings.locations

    def _to_surrounding_point(self, location: Point) -> PointSurroundings:
        _ps = PointSurroundings()
        _ps.location = location
        _ps.distance_to_surroundings = []
        return _ps

    def test_set_buildings_polderside(self):
        # 1. Define test data.
        _buildings_polderside = KoswatSurroundingsPolderside()
        _locations = [
            Point(4.2, 2.4),
            Point(4.2, 4.2),
            Point(2.4, 2.4),
        ]
        _buildings_polderside.points = list(map(self._to_surrounding_point, _locations))
        _surroundings = SurroundingsWrapper()
        assert isinstance(_surroundings, SurroundingsWrapper)

        # 2. Run test.
        _surroundings.buildings_polderside = _buildings_polderside

        # 3. Verify expectations.
        assert isinstance(_surroundings.buildings_polderside, KoswatSurroundingsPolderside)
        assert [x.location for x in _surroundings.locations] == _locations
