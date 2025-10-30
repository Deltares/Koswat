from typing import Callable

import pytest
from shapely import Point

from koswat.dike.surroundings.surroundings_obstacle import SurroundingsObstacle
from koswat.dike.surroundings.wrapper.base_surroundings_wrapper import (
    BaseSurroundingsWrapper,
)
from koswat.dike.surroundings.wrapper.obstacle_surroundings_wrapper import (
    ObstacleSurroundingsWrapper,
)


class TestObstacleSurroundingsWrapper:
    def test_initialize(self):
        # 1. Define wrapper.
        _wrapper = ObstacleSurroundingsWrapper()

        # 2. Verify expectations.
        assert isinstance(_wrapper, ObstacleSurroundingsWrapper)
        assert isinstance(_wrapper, BaseSurroundingsWrapper)

        assert not _wrapper.obstacle_locations

        # Supported surroundings are initialized.
        assert isinstance(_wrapper.buildings, SurroundingsObstacle)
        assert isinstance(_wrapper.railways, SurroundingsObstacle)
        assert isinstance(_wrapper.waters, SurroundingsObstacle)
        assert isinstance(_wrapper.custom_obstacles, SurroundingsObstacle)

    @pytest.mark.parametrize(
        "obstacles_distance",
        [
            pytest.param(24, id="Surroundings WITH obstacles at distance 24"),
            pytest.param(0, id="Surroundings WITHOUT obstacles"),
        ],
    )
    def test_when_get_locations_after_distance_given_safe_obstacles_returns_surrounding_point(
        self,
        obstacles_distance: float,
        buildings_obstacle_surroundings_fixture: Callable[
            [list[tuple[Point, list[float]]]], ObstacleSurroundingsWrapper
        ],
    ):
        # 1. Define test data.
        _location = Point(2.4, 2.4)
        _wrapper = buildings_obstacle_surroundings_fixture(
            [(_location, obstacles_distance)]
        )
        _safe_distance = obstacles_distance - 1

        # 2. Run test.
        _classified_surroundings = _wrapper.get_locations_at_safe_distance(
            _safe_distance
        )

        # 3. Verify expectations.
        assert isinstance(_classified_surroundings, list)
        assert len(_classified_surroundings) == 1
        assert _classified_surroundings[0].location == _location

    def test_when_get_locations_after_distance_given_unsafe_obstacles_returns_nothing(
        self,
        buildings_obstacle_surroundings_fixture: Callable[
            [list[tuple[Point, float]]], ObstacleSurroundingsWrapper
        ],
    ):
        # 1. Define test data.
        _obstacles_distance = 24
        _location = Point(2.4, 2.4)

        _wrapper = buildings_obstacle_surroundings_fixture(
            [(_location, _obstacles_distance)]
        )

        # 2. Run test.
        _classified_surroundings = _wrapper.get_locations_at_safe_distance(
            _obstacles_distance + 1
        )

        # 3. Verify expectations.
        assert isinstance(_classified_surroundings, list)
        assert not any(_classified_surroundings)
