import math
from dataclasses import dataclass
from typing import Callable, Iterator, Type

import pytest
from shapely import Point

from koswat.dike.surroundings.surroundings_obstacle import SurroundingsObstacle
from koswat.dike.surroundings.wrapper.base_surroundings_wrapper import (
    BaseSurroundingsWrapper,
)
from koswat.dike.surroundings.wrapper.obstacle_surroundings_wrapper import (
    ObstacleSurroundingsWrapper,
)
from koswat.dike_reinforcements.reinforcement_profile.reinforcement_room_calculator.reinforcement_room_calculator_protocol import (
    ReinforcementRoomCalculatorProtocol,
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

    @pytest.fixture(name="mocked_room_calculator")
    def get_mocked_room_calculator(
        self,
    ) -> Iterator[Type[ReinforcementRoomCalculatorProtocol]]:
        @dataclass
        class MockedRoomCalculator(ReinforcementRoomCalculatorProtocol):
            return_value: bool

            def reinforcement_has_room(self, *args) -> float:
                return self.return_value

        yield MockedRoomCalculator

    @pytest.mark.parametrize("obstacles_distance", [24, math.nan])
    def test_when_get_locations_after_distance_given_safe_obstacles_returns_surrounding_point(
        self,
        obstacles_distance: float,
        obstacle_buffer: float,
        is_location_safe: bool,
        obstacles_surroundings_fixture: Callable[
            [list[tuple[Point, list[float]]]], ObstacleSurroundingsWrapper
        ],
        mocked_room_calculator: Type[ReinforcementRoomCalculatorProtocol],
    ):
        # 1. Define test data.
        _distance_to_check = 18

        _location = Point(2.4, 2.4)
        _wrapper = obstacles_surroundings_fixture([(_location, obstacles_distance)])

        # 2. Run test.
        _classified_surroundings = _wrapper.get_locations_at_safe_distance(
            mocked_room_calculator(True)
        )

        # 3. Verify expectations.
        assert isinstance(_classified_surroundings, list)
        assert len(_classified_surroundings) == 1
        assert _classified_surroundings[0].location == _location

    def test_when_get_locations_after_distance_given_unsafe_obstacles_returns_nothing(
        self,
        obstacles_surroundings_fixture: Callable[
            [list[tuple[Point, float]]], ObstacleSurroundingsWrapper
        ],
        mocked_room_calculator: Type[ReinforcementRoomCalculatorProtocol],
    ):
        # 1. Define test data.
        _obstacles_distance = 24
        _location = Point(2.4, 2.4)

        _wrapper = obstacles_surroundings_fixture([(_location, _obstacles_distance)])

        # 2. Run test.
        _classified_surroundings = _wrapper.get_locations_at_safe_distance(
            mocked_room_calculator(False)
        )

        # 3. Verify expectations.
        assert isinstance(_classified_surroundings, list)
        assert not any(_classified_surroundings)

    def test_when_obstacle_surroundings_correct_distance_calculated(
        self,
    ):
        # 1. Define test data.
        _location = Point(1.0, 1.0)
        _obstacles_distance = 5

        _wrapper = ObstacleSurroundingsWrapper(
            obstacles=SurroundingsObstacle(
                points=[
                    PointObstacleSurroundings(
                        location=_location,
                        inside_distance=float(_obstacles_distance),
                    )
                ]
            ),
        )

        # 2. Run test.
        _obstacle_locations = _wrapper.obstacles.points

        # 3. Verify expectations.
        assert isinstance(_obstacle_locations, list)
        assert len(_obstacle_locations) == 1
        assert _obstacle_locations[0].location == _location
