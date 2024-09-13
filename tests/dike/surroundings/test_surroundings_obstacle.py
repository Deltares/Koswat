from typing import Callable

import pytest
from shapely import Point

from koswat.dike.surroundings.koswat_surroundings_protocol import (
    KoswatSurroundingsProtocol,
)
from koswat.dike.surroundings.point.point_surroundings import PointSurroundings
from koswat.dike.surroundings.surroundings_obstacle import SurroundingsObstacle


class TestSurroundingsObstacle:
    def test_initialize(self):
        # 1. Initialize
        _surrounding = SurroundingsObstacle()

        # 2. Verify expectations
        assert isinstance(_surrounding, SurroundingsObstacle)
        assert isinstance(_surrounding, KoswatSurroundingsProtocol)
        assert isinstance(_surrounding.points, list)
        assert len(_surrounding.points) == 0

    @pytest.mark.parametrize(
        "obstacles_distance_list",
        [
            pytest.param([24], id="Surroundings WITH obstacles at distance 24"),
            pytest.param([], id="Surroundings WITHOUT obstacles"),
        ],
    )
    def test_when_get_locations_after_distance_given_safe_obstacles_returns_surrounding_point(
        self,
        obstacles_distance_list: list[float],
        distances_to_surrounding_point_builder: Callable[
            [Point, list[float]], PointSurroundings
        ],
    ):
        # 1. Define test data.
        _surrounding_point = distances_to_surrounding_point_builder(
            Point(2.4, 2.4), obstacles_distance_list
        )
        _safe_distance = min(obstacles_distance_list, default=0) - 1
        _surrounding = SurroundingsObstacle(points=[_surrounding_point])

        # 2. Run test.
        _classified_surroundings = _surrounding.get_locations_after_distance(
            _safe_distance
        )

        # 3. Verify expectations.
        assert isinstance(_classified_surroundings, list)
        assert len(_classified_surroundings) == 1
        assert _classified_surroundings[0] == _surrounding_point

    def test_when_get_locations_after_distance_given_unsafe_obstacles_returns_nothing(
        self,
        distances_to_surrounding_point_builder: Callable[
            [Point, list[float]], PointSurroundings
        ],
    ):
        # 1. Define test data.
        _obstacles_distance_list = [24]
        _surrounding_point = distances_to_surrounding_point_builder(
            Point(2.4, 2.4), _obstacles_distance_list
        )
        _surrounding = SurroundingsObstacle(points=[_surrounding_point])

        # 2. Run test.
        _classified_surroundings = _surrounding.get_locations_after_distance(
            min(_obstacles_distance_list) + 1
        )

        # 3. Verify expectations.
        assert isinstance(_classified_surroundings, list)
        assert not any(_classified_surroundings)
