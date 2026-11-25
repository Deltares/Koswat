import copy
from collections.abc import Iterator
from typing import Callable

import pytest

from koswat.dike.surroundings.point import PointInfrastructureSurroundings
from koswat.dike_reinforcements.reinforcement_profile import (
    CofferdamReinforcementProfile,
    SoilReinforcementProfile,
    StabilityWallCrestReinforcementProfile,
)
from koswat.dike_reinforcements.reinforcement_profile.reinforcement_profile_protocol import (
    ReinforcementProfileProtocol,
)
from koswat.dike_reinforcements.reinforcement_profile.standard.soil_waterside_reinforcement_profile import (
    SoilWatersideReinforcementProfile,
)
from koswat.strategies.order_strategy.order_strategy import OrderStrategy
from koswat.strategies.strategy_input import StrategyInput
from koswat.strategies.strategy_location_input import StrategyLocationInput
from koswat.strategies.strategy_location_reinforcement import (
    StrategyLocationReinforcement,
)
from koswat.strategies.strategy_reinforcement_input import (
    StrategyReinforcementInputBuilder,
)
from koswat.strategies.strategy_reinforcement_input.strategy_reinforcement_input_protocol import (
    StrategyReinforcementInputProtocol,
)
from koswat.strategies.strategy_reinforcement_type_costs import (
    StrategyReinforcementTypeCosts,
)
from koswat.strategies.strategy_reinforcement_widths import StrategyReinforcementWidths


def _get_example_strategy_input(exclude_waterside: bool):
    # This is the data defined in the docs\reference\koswat_strategies.md
    # as examples. DON'T MODIFY IT!
    _initial_state_per_location = [
        SoilReinforcementProfile,  # Expected idx 0 in default order!
        SoilReinforcementProfile,
        SoilReinforcementProfile,
        StabilityWallCrestReinforcementProfile,  # Expected idx 4 in default order!
        StabilityWallCrestReinforcementProfile,
        SoilReinforcementProfile,
        SoilReinforcementProfile,
        SoilReinforcementProfile,
        CofferdamReinforcementProfile,  # Expected idx 5 in default order!
        CofferdamReinforcementProfile,
    ]

    _reinforcement_type_default_order = (
        OrderStrategy.get_default_order_for_reinforcements()
    )

    # Make sure some reinforment types don't influence the infra strategy.
    if exclude_waterside:
        _waterside_soil_reinforcement_idx = _reinforcement_type_default_order.index(
            SoilWatersideReinforcementProfile
        )
        _reinforcement_type_default_order.pop(_waterside_soil_reinforcement_idx)
        _base_cost_multipliers = [0, 0.5, 1, 1.5, 2, 3]
    else:
        _base_cost_multipliers = [0, 0.25, 0.5, 1, 1.5, 2, 3]

    assert len(_base_cost_multipliers) == len(
        _reinforcement_type_default_order
    ), "The base cost multipliers must match the number of reinforcement types in the default order."

    _levels_data = [
        StrategyReinforcementTypeCosts(
            reinforcement_type=_reinforcement,
            base_costs_with_surtax=(10 ** _base_cost_multipliers[_idx]) * 42.0,
            infrastructure_costs_with_surtax=(
                4.2e5 if _idx in [0, 1, 3, 4] else 0.0
            ),  # Dramatic infra costs so they move to where we want
        )
        for _idx, _reinforcement in enumerate(_reinforcement_type_default_order)
    ]

    _initial_states = {
        _srtc.reinforcement_type: _levels_data[_idx:]
        for _idx, _srtc in enumerate(_levels_data)
    }

    _strategy_locations = [
        StrategyLocationInput(
            point_surrounding=PointInfrastructureSurroundings(traject_order=_idx),
            strategy_reinforcement_type_costs=copy.deepcopy(_initial_states[_rt]),
        )
        for _idx, _rt in enumerate(_initial_state_per_location)
    ]
    _strategy_reinforcements = [
        StrategyReinforcementInputBuilder(
            reinforcement_type=_rtc.reinforcement_type,
            active=True,
            base_costs_with_surtax=_rtc.base_costs_with_surtax,
            ground_level_surface=10.0 * (len(_reinforcement_type_default_order) - _idx),
            reinforcement_widths=StrategyReinforcementWidths(
                width_polderside=50, width_waterside=25
            ),
        ).build()
        for _idx, _rtc in enumerate(_levels_data)
    ]

    return StrategyInput(
        strategy_locations=_strategy_locations,
        strategy_reinforcements=_strategy_reinforcements,
        reinforcement_min_buffer=1,
        reinforcement_min_length=5,
        waterside_reinforcement_allowed=not exclude_waterside,
    )


@pytest.fixture(name="example_strategy_input_generator")
def _get_example_strategy_input_generator() -> Callable[[bool], StrategyInput]:
    def get_strategy_input(exclude_waterside: bool) -> StrategyInput:
        return _get_example_strategy_input(exclude_waterside)

    return get_strategy_input


@pytest.fixture(name="example_strategy_input")
def _get_example_strategy_input_without_waterside_soil_reinforcement(
    example_strategy_input_generator,
) -> Iterator[StrategyInput]:
    yield example_strategy_input_generator(True)


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
        == 6
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


@pytest.fixture(name="example_default_order", scope="session")
def _get_example_default_order() -> list[type[ReinforcementProfileProtocol]]:
    _reinforcement_order = OrderStrategy.get_default_order_for_reinforcements()
    return _exclude_waterside_soil_reinforcement(_reinforcement_order)


def _exclude_waterside_soil_reinforcement(
    strategy_reinforcements: list[StrategyReinforcementInputProtocol],
) -> list[StrategyReinforcementInputProtocol]:
    _idx = strategy_reinforcements.index(SoilWatersideReinforcementProfile)
    strategy_reinforcements.pop(_idx)
    return strategy_reinforcements


@pytest.fixture(name="example_location_reinforcements_with_buffering")
def _get_example_location_reinforcements_with_buffering(
    example_strategy_input: StrategyInput,
    example_default_order: list[type[ReinforcementProfileProtocol]],
) -> Iterator[list[StrategyLocationReinforcement]]:
    _result_after_buffering_idx = [0, 0, 3, 3, 3, 3, 0, 4, 4, 4]
    _location_reinforcements = []
    for _idx, _location in enumerate(example_strategy_input.strategy_locations):
        _measure_idx = _result_after_buffering_idx[_idx]
        _location_reinforcements.append(
            StrategyLocationReinforcement(
                location=_location,
                available_measures=[example_default_order[_measure_idx]],
                filtered_measures=[example_default_order[_measure_idx]],
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
    #     (4, ["Location_002","Location_003", "Location_004",]),
    #     (5, ["Location_005","Location_006", "Location_007",
    #           "Location_008","Location_009",]),
    # }
    # Clean up previous costs.
    for _sl in example_strategy_input.strategy_locations:
        for _cost in _sl.strategy_reinforcement_type_costs:
            _cost.infrastructure_costs = 0
            _cost.infrastructure_costs_with_surtax = 0

    def modify_costs_to(
        location: StrategyLocationInput,
        target_reinforcement_idx: int,
    ):
        # We only modify the infra costs because the base costs increment
        # with the index, so reinforcement_type[5].base_costs > reinforcement_type[4].base_costs
        for _costs in location.strategy_reinforcement_type_costs[
            :target_reinforcement_idx
        ]:
            _costs.infrastructure_costs = 4.2e5
            _costs.infrastructure_costs_with_surtax = _costs.infrastructure_costs * 2

    # We force the first cluster from index 0 to index 2
    modify_costs_to(example_strategy_input.strategy_locations[0], 2)
    # We split the second cluster, so that the second (minimal half) is increased to index 5
    modify_costs_to(example_strategy_input.strategy_locations[5], 5)
    yield example_strategy_input
