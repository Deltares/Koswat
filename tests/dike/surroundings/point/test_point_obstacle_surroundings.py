import math
from koswat.dike.surroundings.point.point_obstacle_surroundings import PointObstacleSurroundings
from koswat.dike.surroundings.point.point_surroundings import PointSurroundings


class TestPointObstacleSurroundings:
    def test_initialize_point_obstacle_surroundings(self):
        # 1. Define test data.
        _pos = PointObstacleSurroundings()
        
        # 2. Verify expectations.
        assert isinstance(_pos, PointObstacleSurroundings)
        assert isinstance(_pos, PointSurroundings)
        assert not _pos.section
        assert not _pos.location
        assert not _pos.surroundings_matrix
        assert math.isnan(_pos.inside_distance)
        assert math.isnan(_pos.outside_distance)
        assert math.isnan(_pos.angle_inside)
        assert math.isnan(_pos.angle_outside)
        assert math.isnan(_pos.closest_obstacle)

    def test_closest_obstacle_returns_inside_distance(self):
        # 1. Define test data.
        _inside_distance = 246.01

        # 2. Run test
        _pos = PointObstacleSurroundings(
            inside_distance=_inside_distance
        )
        
        # 2. Verify expectations.
        assert _pos.closest_obstacle == _inside_distance


    def test_merge_point_obstacle_surroundings(self):
        # 1. Define test data.
        _pos_1 = PointObstacleSurroundings(
            inside_distance=10.0,
            outside_distance=20.0,
            angle_inside=30.0,
            angle_outside=40.0,
        )
        _pos_2 = PointObstacleSurroundings(
            inside_distance=5.0,
            outside_distance=25.0,
            angle_inside=15.0,
            angle_outside=35.0,
        )

        # 2. Run test
        _pos_1.merge(_pos_2)

        # 3. Verify expectations.
        # It should always get the min between both of them.
        assert _pos_1.inside_distance == 5.0
        assert _pos_1.outside_distance == 20.0
        assert _pos_1.angle_inside == 15.0
        assert _pos_1.angle_outside == 35.0
    
    def test_merge_point_obstacle_surroundings_with_nan(self):
        # 1. Define test data.
        _pos_1 = PointObstacleSurroundings(
            inside_distance=math.nan,
            outside_distance=20.0,
            angle_inside=math.nan,
            angle_outside=40.0,
        )
        _pos_2 = PointObstacleSurroundings(
            inside_distance=5.0,
            outside_distance=math.nan,
            angle_inside=15.0,
            angle_outside=math.nan,
        )

        # 2. Run test
        _pos_1.merge(_pos_2)

        # 3. Verify expectations.
        # It should always get the min between both of them.
        assert _pos_1.inside_distance == 5.0
        assert _pos_1.outside_distance == 20.0
        assert _pos_1.angle_inside == 15.0
        assert _pos_1.angle_outside == 40.0