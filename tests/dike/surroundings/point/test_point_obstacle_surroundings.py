import math

import pytest
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

    @pytest.mark.parametrize(
            "inside_distance, outside_distance, expected_result",
            [
                pytest.param(100.0, 200.0, 100, id="inside_smaller"),
                pytest.param(200.0, 100.0, 100, id="outside_smaller"),
                pytest.param(math.nan, 300.0, 300, id="inside_nan"),
                pytest.param(400.0, math.nan, 400, id="outside_nan"),
            ]
    )
    def test_when_closest_obstacle_given_inside_and_outside_distances_then_smallest_number_returned(self, inside_distance: float, outside_distance: float, expected_result: float) -> float:
        # 1. Run test
        _pos = PointObstacleSurroundings(
            inside_distance=inside_distance,
            outside_distance=outside_distance
        )
        
        assert _pos.closest_obstacle == expected_result

    def test_when_closest_obstacle_given_inside_and_outside_distances_are_nan_then_returns_nan(self):
        # 1. Run test
        _pos = PointObstacleSurroundings(
            inside_distance=math.nan,
            outside_distance=math.nan
        )

        # 2. Verify expectations.
        assert math.isnan(_pos.closest_obstacle)

    def test_when_merge_given_two_point_obstacle_surroundings_then_sets_the_min_distances(self):
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
    
    def test_when_merge_given_point_obstacle_surroundings_with_nan_then_sets_non_nan_values(self):
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

    def test_when_obstacle_free_room_given_nan_values_then_fallback_is_used(self):
        # 1. Define test data.
        _fallback_value = 500
        _pos = PointObstacleSurroundings(
            inside_distance=math.nan,
            outside_distance=math.nan
        )

        # 2. Verify expectations.
        assert _pos.obstacle_free_room == _fallback_value * 2

    @pytest.mark.parametrize(
        "inside_distance, outside_distance, expected_value",
        [
            pytest.param(100.0, 200.0, 300, id="both_valid"),
            pytest.param(math.nan, 200.0, 700, id="outside_nan_uses_fallback_500m"),
            pytest.param(100.0, math.nan, 600, id="inside_nan_uses_fallback_500m"),
        ]
    )
    def test_when_obstacle_free_room_given_valid_values_then_returns_addition_of_both(self, inside_distance: float, outside_distance: float, expected_value: float):
        # 1. Define test data.
        _pos = PointObstacleSurroundings(
            inside_distance=inside_distance,
            outside_distance=outside_distance
        )

        # 2. Verify expectations.
        assert _pos.obstacle_free_room == expected_value