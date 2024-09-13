import math

from koswat.dike.surroundings.point.point_surroundings import PointSurroundings


class TestPointSurroundings:
    def test_initialize_point_surroundings(self):
        _p_s = PointSurroundings()
        assert isinstance(_p_s, PointSurroundings)
        assert not _p_s.section
        assert not _p_s.location
        assert not _p_s.surroundings_matrix
        assert math.isnan(_p_s.closest_obstacle)

    def test_closest_building_returns_min_value(self):
        _p_s = PointSurroundings()
        _p_s.surroundings_matrix = {42: 1, 24: 1, 2.4: 0}
        assert _p_s.closest_obstacle == 24
