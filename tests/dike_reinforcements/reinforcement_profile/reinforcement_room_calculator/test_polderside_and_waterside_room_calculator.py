import pytest
from koswat.dike.surroundings.point.point_obstacle_surroundings import PointObstacleSurroundings
from koswat.dike_reinforcements.reinforcement_profile.reinforcement_room_calculator.polderside_and_waterside_room_calculator import PoldersideAndWatersideRoomCalculator
from koswat.dike_reinforcements.reinforcement_profile.reinforcement_room_calculator.reinforcement_room_calculator_base import ReinforcementRoomCalculatorBase
from koswat.dike_reinforcements.reinforcement_profile.reinforcement_room_calculator.reinforcement_room_calculator_protocol import ReinforcementRoomCalculatorProtocol

def get_reinforcement_and_obstacle_room_cases() -> list[pytest.param]:
    _polderside_width = 4
    _waterside_width = 2
    _base_calculator = PoldersideAndWatersideRoomCalculator(
                required_polderside_width=_polderside_width,
                required_waterside_width=_waterside_width
            )
    
    def get_point_obstacle_surroundings(inside_space: float, outside_space: float) -> PointObstacleSurroundings:
        return PointObstacleSurroundings(
            inside_distance=inside_space,
            outside_distance=outside_space
        )

    return [
        pytest.param(
            _base_calculator,
            get_point_obstacle_surroundings(_polderside_width, _waterside_width),
            True,
            id="exact_room_at_both_sides"
        ),
        pytest.param(
            _base_calculator,
            get_point_obstacle_surroundings(_polderside_width + 1, _waterside_width + 1),
            True,
            id="enough_room_at_both_sides"
        ),
        pytest.param(
            _base_calculator,
            get_point_obstacle_surroundings(_polderside_width + _waterside_width, 0),
            True,
            id="enough_room_only_at_polderside"
        ),
        pytest.param(
            _base_calculator,
            get_point_obstacle_surroundings(0, _polderside_width + _waterside_width),
            True,
            id="enough_room_only_at_waterside"
        ),
        pytest.param(
            _base_calculator,
            get_point_obstacle_surroundings(_polderside_width - 2, _waterside_width + 2),
            True,
            id="more_room_on_the_waterside"
        ),
        pytest.param(
            _base_calculator,
            get_point_obstacle_surroundings(_polderside_width + 1, _waterside_width - 1),
            True,
            id="more_room_on_the_polderside"
        ),
        pytest.param(
            _base_calculator,
            get_point_obstacle_surroundings(_polderside_width - 1, _waterside_width - 1),
            False,
            id="not_enough_room_at_either_side"
        )
    ]

reinforcement_point_obstacle_cases = get_reinforcement_and_obstacle_room_cases()

class TestPoldersideAndWatersideRoomCalculator:

    def test_when_initialize_then_returns_instance(self):
        # 1. When
        _calculator = PoldersideAndWatersideRoomCalculator(
            required_polderside_width=1.0,
            required_waterside_width=2.0
        )

        # 2. Then
        assert isinstance(_calculator, PoldersideAndWatersideRoomCalculator)
        assert isinstance(_calculator, ReinforcementRoomCalculatorBase)
        assert isinstance(_calculator, ReinforcementRoomCalculatorProtocol)

    def test_when__required_width_given_calculator_then_returns_summation_of_widths(self):
        # 1. Given
        _polderside_width = 1.0
        _waterside_width = 2.0
        _calculator = PoldersideAndWatersideRoomCalculator(
            required_polderside_width=_polderside_width,
            required_waterside_width=_waterside_width
        )

        # 2. When
        result = _calculator._required_width

        # 3. Then
        assert result == (_polderside_width + _waterside_width)


    @pytest.mark.parametrize("calculator, surroundings, expected_result", reinforcement_point_obstacle_cases)
    def test_when_reinforcement_has_room_given_point_obstacle_surroundings_then_returns_expectation(self, calculator: PoldersideAndWatersideRoomCalculator, surroundings: PointObstacleSurroundings, expected_result: bool):
        # 1. Given
        assert isinstance(calculator, PoldersideAndWatersideRoomCalculator)
        assert isinstance(surroundings, PointObstacleSurroundings)

        # 2. When
        _result = calculator.reinforcement_has_room(surroundings, True)

        # 3. Then
        assert _result == expected_result

    def test_when_reinforcement_has_room_given_only_waterside_space_and_cannot_use_waterside_then_returns_false(self):
        # 1. Given
        _can_use_waterside = False
        _polderside_width = 1.0
        _waterside_width = 2.0
        _calculator = PoldersideAndWatersideRoomCalculator(
            required_polderside_width=_polderside_width,
            required_waterside_width=_waterside_width
        )

        _surroundings = PointObstacleSurroundings(
            inside_distance=0,
            outside_distance=1000
        )

        # 2. When
        _result = _calculator.reinforcement_has_room(_surroundings, _can_use_waterside)

        # 3. Then
        assert _result == False
