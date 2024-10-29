from typing import Iterator

import pytest

from koswat.dike.surroundings.point.point_surroundings import PointSurroundings
from koswat.dike_reinforcements.reinforcement_profile import (
    CofferdamReinforcementProfile,
    SoilReinforcementProfile,
    StabilityWallReinforcementProfile,
)
from koswat.strategies.order_strategy.order_strategy import OrderStrategy
from koswat.strategies.strategy_input import StrategyInput
from koswat.strategies.strategy_location_input import StrategyLocationInput
from koswat.strategies.strategy_location_reinforcement import (
    StrategyLocationReinforcement,
)
from koswat.strategies.strategy_reinforcement_input import StrategyReinforcementInput
from koswat.strategies.strategy_reinforcement_type_costs import (
    StrategyReinforcementTypeCosts,
)


@pytest.fixture(name="example_strategy_input")
def _get_example_strategy_input() -> Iterator[StrategyInput]:
    # This is the data defined in the docs\reference\koswat_strategies.md
    # as examples. DON'T MODIFY IT!
    _initial_state_per_location = [
        SoilReinforcementProfile,  # Expected idx 0 in default order!
        SoilReinforcementProfile,
        SoilReinforcementProfile,
        StabilityWallReinforcementProfile,  # Expected idx 3 in default order!
        StabilityWallReinforcementProfile,
        SoilReinforcementProfile,
        SoilReinforcementProfile,
        SoilReinforcementProfile,
        CofferdamReinforcementProfile,  # Expected idx 4 in default order!
        CofferdamReinforcementProfile,
    ]

    _reinforcement_type_default_order = (
        OrderStrategy.get_default_order_for_reinforcements()
    )
    _levels_data = [
        StrategyReinforcementTypeCosts(
            reinforcement_type=_reinforcement,
            base_costs=(10**_idx) * 42.0,
            infrastructure_costs=(10 ** (len(_reinforcement_type_default_order) - 1))
            * 42.0
            if _idx in [0, 1, 3]
            else 0.0,  # Dramatic infra costs so they move to where we want
        )
        for _idx, _reinforcement in enumerate(_reinforcement_type_default_order)
    ]

    _initial_states = {
        _srtc.reinforcement_type: _levels_data[_idx:]
        for _idx, _srtc in enumerate(_levels_data)
    }

    _strategy_locations = [
        StrategyLocationInput(
            point_surrounding=PointSurroundings(traject_order=_idx),
            strategy_reinforcement_type_costs=_initial_states[_rt],
        )
        for _idx, _rt in enumerate(_initial_state_per_location)
    ]
    _strategy_reinforcements = [
        StrategyReinforcementInput(
            reinforcement_type=_rtc.reinforcement_type,
            base_costs=_rtc.base_costs,
            ground_level_surface=10.0 * (len(_reinforcement_type_default_order) - _idx),
        )
        for _idx, _rtc in enumerate(_levels_data)
    ]

    yield StrategyInput(
        strategy_locations=_strategy_locations,
        strategy_reinforcements=_strategy_reinforcements,
        reinforcement_min_buffer=1,
        reinforcement_min_length=5,
    )


@pytest.fixture(name="example_location_input")
def _get_example_location_input(
    example_strategy_input: StrategyInput,
) -> Iterator[list[StrategyLocationInput]]:
    assert any(example_strategy_input.strategy_locations)
    assert (
        len(
            example_strategy_input.strategy_locations[
                0
            ].strategy_reinforcement_type_costs
        )
        == 5
    )
    assert (
        len(
            example_strategy_input.strategy_locations[
                -1
            ].strategy_reinforcement_type_costs
        )
        == 1
    )
    assert (
        example_strategy_input.strategy_locations[-1]
        .strategy_reinforcement_type_costs[0]
        .reinforcement_type
        != SoilReinforcementProfile
    )
    yield example_strategy_input.strategy_locations


@pytest.fixture(name="example_location_reinforcements_with_buffering")
def _get_example_location_reinforcements_with_buffering(
    example_strategy_input: StrategyInput,
) -> Iterator[list[StrategyLocationReinforcement]]:
    _result_after_buffering_idx = [0, 0, 3, 3, 3, 3, 0, 4, 4, 4]
    _measure_order = OrderStrategy.get_default_order_for_reinforcements()
    _location_reinforcements = []
    for _idx, _location in enumerate(example_strategy_input.strategy_locations):
        _measure_idx = _result_after_buffering_idx[_idx]
        _location_reinforcements.append(
            StrategyLocationReinforcement(
                location=_location,
                selected_measure=_measure_order[_measure_idx],
                available_measures=[],
            )
        )

    yield _location_reinforcements
