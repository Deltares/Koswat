import copy
from typing import Iterator

import pytest

from koswat.dike.surroundings.point.point_surroundings import PointSurroundings
from koswat.dike_reinforcements.reinforcement_profile.outside_slope.cofferdam_reinforcement_profile import (
    CofferdamReinforcementProfile,
)
from koswat.dike_reinforcements.reinforcement_profile.standard.soil_reinforcement_profile import (
    SoilReinforcementProfile,
)
from koswat.dike_reinforcements.reinforcement_profile.standard.stability_wall_reinforcement_profile import (
    StabilityWallReinforcementProfile,
)
from koswat.strategies.order_strategy.order_strategy import OrderStrategy
from koswat.strategies.strategy_input import StrategyInput
from koswat.strategies.strategy_location_input import StrategyLocationInput
from koswat.strategies.strategy_location_reinforcement import (
    StrategyLocationReinforcement,
)
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
            base_costs=(10**_idx) * 42,
            infrastructure_costs=(10 ** (len(_reinforcement_type_default_order) - 1))
            * 42
            if _idx in [0, 1, 3]
            else 0,  # Dramatic infra costs so they move to where we want
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
            strategy_reinforcement_type_costs=copy.deepcopy(_initial_states[_rt]),
        )
        for _idx, _rt in enumerate(_initial_state_per_location)
    ]

    yield StrategyInput(
        strategy_locations=_strategy_locations,
        reinforcement_min_buffer=1,
        reinforcement_min_length=5,
    )


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


@pytest.fixture(name="example_subclustering")
def _get_example_location_reinforcements_with_selected_subclustering(
    example_strategy_input: StrategyInput,
) -> Iterator[StrategyInput]:
    # Force min cluster to be our required value.
    example_strategy_input.reinforcement_min_buffer = 0.5
    assert (
        example_strategy_input.reinforcement_min_cluster == 2
    ), "Test should be written under fake data for demonstration purposes."

    # Only apply infrastructure costs at position 0 and 5 ( `Location_005`)
    # This should induce a splitting of the second cluster (based on order strategy)
    # so that the final result should be:
    # {
    #     (2, ["Location_000","Location_001",]),
    #     (3, ["Location_002","Location_003", "Location_004",]),
    #     (4, ["Location_005","Location_006", "Location_007",
    #           "Location_008","Location_009",]),
    # }
    # Clean up previous costs.
    for _sl in example_strategy_input.strategy_locations:
        for _cost in _sl.strategy_reinforcement_type_costs:
            _cost.infrastructure_costs = 0

    def modify_costs_to(
        location: StrategyLocationInput,
        target_reinforcement_idx: int,
    ):
        _reinforcement_type_default_order = (
            OrderStrategy.get_default_order_for_reinforcements()
        )
        # We only modify the infra costs because the base costs increment
        # with the index, so reinforcement_type[4].base_costs > reinforcement_type[3].base_costs
        for _costs in location.strategy_reinforcement_type_costs[
            :target_reinforcement_idx
        ]:
            _costs.infrastructure_costs = (
                10 ** len(_reinforcement_type_default_order)
            ) * 42

    # We force the first cluster from index 0 to index 2
    modify_costs_to(example_strategy_input.strategy_locations[0], 2)
    # We split the second cluster, so that the second (minimal half) is increased to index 4
    modify_costs_to(example_strategy_input.strategy_locations[5], 4)
    yield example_strategy_input
