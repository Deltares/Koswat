import math
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

        assert not any(_wrapper.obstacles.points)

        # Supported surroundings are initialized.
        assert isinstance(_wrapper.obstacles, SurroundingsObstacle)

    @pytest.mark.parametrize(
        "obstacles_distance, obstacle_buffer, is_location_safe",
        [
            pytest.param(
                math.nan, 20, True, id="Surroundings without obstacles, safe location"
            ),
            pytest.param(
                25, 5, True, id="Obstacle with buffer > distance, safe location"
            ),
            pytest.param(
                20, 0, True, id="Obstacle without buffer > distance, safe location"
            ),
            pytest.param(
                20, 5, False, id="Obstacle with buffer < distance, unsafe location"
            ),
            pytest.param(
                15, 0, False, id="Obstacle without buffer < distance, unsafe location"
            ),
        ],
    )
    def test_when_get_locations_after_distance_given_obstacle_with_bufferr_returns_safe_point(
        self,
        obstacles_distance: float,
        obstacle_buffer: float,
        is_location_safe: bool,
        obstacles_surroundings_fixture: Callable[
            [list[tuple[Point, list[float]]]], ObstacleSurroundingsWrapper
        ],
    ):
        # 1. Define test data.
        _distance_to_check = 18

        _location = Point(2.4, 2.4)
        _wrapper = obstacles_surroundings_fixture([(_location, obstacles_distance)])
        _wrapper.obstacle_buffer = obstacle_buffer

        # 2. Run test.
        _classified_surroundings = _wrapper.get_locations_at_safe_distance(
            _distance_to_check
        )

        # 3. Verify expectations.
        assert isinstance(_classified_surroundings, list)
        assert (len(_classified_surroundings) > 0) == is_location_safe
