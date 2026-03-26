import math

import pytest

from koswat.dike.surroundings.point.point_obstacle_surroundings import (
    PointObstacleSurroundings,
)
from koswat.dike_reinforcements.reinforcement_profile.reinforcement_room_calculator.polderside_only_room_calculator import (
    PoldersideOnlyRoomCalculator,
)
from koswat.dike_reinforcements.reinforcement_profile.reinforcement_room_calculator.reinforcement_room_calculator_base import (
    ReinforcementRoomCalculatorBase,
)
from koswat.dike_reinforcements.reinforcement_profile.reinforcement_room_calculator.reinforcement_room_calculator_protocol import (
    ReinforcementRoomCalculatorProtocol,
)


def get_reinforcement_and_obstacle_room_cases() -> list[pytest.param]:
    _polderside_width = 4
    _waterside_width = 2
    _base_calculator = PoldersideOnlyRoomCalculator(
        required_polderside_width=_polderside_width
    )
    return [
        pytest.param(
            _base_calculator,
            PointObstacleSurroundings(inside_distance=_polderside_width),
            True,
            id="exact_room",
        ),
        pytest.param(
            _base_calculator,
            PointObstacleSurroundings(inside_distance=_polderside_width + 1),
            True,
            id="enough_room",
        ),
        pytest.param(
            _base_calculator,
            PointObstacleSurroundings(
                inside_distance=_polderside_width + _waterside_width, outside_distance=0
            ),
            True,
            id="enough_room_only_at_polderside",
        ),
        pytest.param(
            _base_calculator,
            PointObstacleSurroundings(
                outside_distance=_polderside_width + _waterside_width, inside_distance=0
            ),
            False,
            id="enough_room_only_at_waterside",
        ),
        pytest.param(
            _base_calculator,
            PointObstacleSurroundings(
                inside_distance=_polderside_width - 1,
                outside_distance=_waterside_width - 1,
            ),
            False,
            id="not_enough_room_at_either_side",
        ),
    ]


reinforcement_point_obstacle_cases = get_reinforcement_and_obstacle_room_cases()


class TestPoldersideOnlyRoomCalculator:

    def test_when_initialize_then_returns_instance(self):
        # 1. When
        _calculator = PoldersideOnlyRoomCalculator(required_polderside_width=1.0)

        # 2. Then
        assert isinstance(_calculator, PoldersideOnlyRoomCalculator)
        assert isinstance(_calculator, ReinforcementRoomCalculatorBase)
        assert isinstance(_calculator, ReinforcementRoomCalculatorProtocol)

    def test_when__required_width_given_calculator_then_returns_polderside_width(self):
        # 1. Given
        _polderside_width = 1.0
        _calculator = PoldersideOnlyRoomCalculator(
            required_polderside_width=_polderside_width
        )

        # 2. When
        result = _calculator._required_width

        # 3. Then
        assert result == _polderside_width

    @pytest.mark.parametrize(
        "calculator, surroundings, expected_result", reinforcement_point_obstacle_cases
    )
    def test_when_reinforcement_has_room_given_point_obstacle_surroundings_then_returns_expectation(
        self,
        calculator: PoldersideOnlyRoomCalculator,
        surroundings: PointObstacleSurroundings,
        expected_result: bool,
    ):
        # 1. Given
        assert isinstance(calculator, PoldersideOnlyRoomCalculator)
        assert isinstance(surroundings, PointObstacleSurroundings)

        # 2. When
        _result = calculator.reinforcement_has_room(surroundings)

        # 3. Then
        assert _result == expected_result

    @pytest.mark.parametrize(
        "obstacle_distance, obstacle_buffer, is_location_safe",
        [
            pytest.param(
                25, 4, True, id="Obstacle with buffer > distance, safe location"
            ),
            pytest.param(
                20, 0, True, id="Obstacle without buffer > distance, safe location"
            ),
            pytest.param(
                20, 2, True, id="Obstacle with buffer == distance, safe location"
            ),
            pytest.param(
                20, 4, False, id="Obstacle with buffer < distance, unsafe location"
            ),
            pytest.param(
                15, 0, False, id="Obstacle without buffer < distance, unsafe location"
            ),
        ],
    )
    def test_when_reinforcement_has_room_given_point_obstacle_surroundings_with_buffer_then_returns_expectation(
        self, obstacle_distance: float, obstacle_buffer: float, is_location_safe: bool
    ):
        # 1. Given
        _distance_to_check = 18

        _calculator = PoldersideOnlyRoomCalculator(
            required_polderside_width=_distance_to_check
        )
        _surroundings = PointObstacleSurroundings(inside_distance=obstacle_distance)

        # 2. When
        _result = _calculator.reinforcement_has_room(_surroundings, obstacle_buffer)

        # 3. Then
        assert _result == is_location_safe
