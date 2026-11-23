import math

import pytest

from koswat.dike.surroundings.point import (
    PointInfrastructureSurroundings,
    PointObstacleSurroundings,
    PointSurroundingsProtocol,
)


class TestPointObstacleSurroundings:
    def test_initialize_point_obstacle_surroundings(self):
        # 1. Define test data.
        _pos = PointObstacleSurroundings()

        # 2. Verify expectations.
        assert isinstance(_pos, PointObstacleSurroundings)
        assert isinstance(_pos, PointSurroundingsProtocol)
        assert not _pos.section
        assert not _pos.location
        assert math.isnan(_pos.inside_distance)
        assert math.isnan(_pos.outside_distance)
        assert math.isnan(_pos.angle_inside)
        assert math.isnan(_pos.angle_outside)

    @pytest.mark.parametrize(
        "obstacle_type", [PointObstacleSurroundings, PointInfrastructureSurroundings]
    )
    def test_when_testing_equality_given_comparable_type_then_return_true(
        self, obstacle_type: type[PointSurroundingsProtocol]
    ):
        # Given
        _traject_order = 123
        _this = PointObstacleSurroundings(traject_order=_traject_order)
        _other = obstacle_type()
        _other.traject_order = _traject_order

        # When
        result: bool = _this == _other

        # Then
        assert result

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

    def test_when_merge_given_invalid_input_then_raises_type_error(self):
        _pos = PointObstacleSurroundings()
        with pytest.raises(TypeError):
            _pos.merge("invalid_input")
