from typing import Iterator

import pytest

from koswat.dike.surroundings.point.point_surroundings import PointSurroundings
from koswat.dike_reinforcements.input_profile.piping_wall.piping_wall_input_profile import (
    PipingWallInputProfile,
)
from koswat.dike_reinforcements.input_profile.vertical_piping_solution.vps_input_profile import (
    VPSInputProfile,
)
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
    _levels_data = {
        SoilReinforcementProfile: (0, 420000),
        VPSInputProfile: (4.2, 42000),
        PipingWallInputProfile: (42, 4200),
        StabilityWallReinforcementProfile: (420, 42),
        CofferdamReinforcementProfile: (4200, 4.2),
    }

    # This is the data defined in the docs\reference\koswat_strategies.md
    # as examples. DON'T MODIFY IT!
    _initial_state_per_location = [
        SoilReinforcementProfile,
        SoilReinforcementProfile,
        SoilReinforcementProfile,
        StabilityWallReinforcementProfile,
        StabilityWallReinforcementProfile,
        SoilReinforcementProfile,
        SoilReinforcementProfile,
        SoilReinforcementProfile,
        CofferdamReinforcementProfile,
        CofferdamReinforcementProfile,
    ]
    _strategy_locations = []
    for _idx, _rt in enumerate(_initial_state_per_location):
        _levels_idx = list(_levels_data.keys()).index(_rt)
        _available_srtc = list(_levels_data.items())[_levels_idx:]
        _sli = StrategyLocationInput(
            point_surrounding=PointSurroundings(traject_order=_idx),
            strategy_reinforcement_type_costs=[
                StrategyReinforcementTypeCosts(
                    reinforcement_type=_reinforcement_type,
                    base_costs=_costs[0],
                    infastructure_costs=[1],
                )
                for _reinforcement_type, _costs in _available_srtc
            ],
        )
        _strategy_locations.append(_sli)
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


@pytest.fixture(name="example_strategy_input_with_infra_costs")
def _get_example_strategy_input_with_infra_costs_for_unbalanced_clusters(
    example_strategy_input: StrategyInput,
) -> Iterator[StrategyInput]:
    for _sl in example_strategy_input.strategy_locations:
        pass
