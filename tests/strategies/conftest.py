from typing import Iterator, Type

import pytest

from koswat.dike.surroundings.point.point_surroundings import PointSurroundings
from koswat.dike_reinforcements.reinforcement_profile.reinforcement_profile_protocol import (
    ReinforcementProfileProtocol,
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
from koswat.strategies.strategy_reinforcement_type import StrategyReinforcementType


@pytest.fixture(name="example_strategy_input")
def _get_example_strategy_input() -> Iterator[StrategyInput]:
    def _to_strategy_location(
        idx: int, reinforcement_type: list[Type[ReinforcementProfileProtocol]]
    ) -> StrategyLocationInput:
        return StrategyLocationInput(
            point_surrounding=PointSurroundings(traject_order=idx),
            strategy_reinforcement_type=[
                StrategyReinforcementType(reinforcement_type=_rt)
                for _rt in reinforcement_type
            ],
        )

    # This is the data defined in the docs\reference\koswat_strategies.md
    # as examples. DON'T MODIFY IT!
    _initial_state_per_location = [
        [SoilReinforcementProfile],
        [SoilReinforcementProfile],
        [SoilReinforcementProfile],
        [StabilityWallReinforcementProfile],
        [StabilityWallReinforcementProfile],
        [SoilReinforcementProfile],
        [SoilReinforcementProfile],
        [SoilReinforcementProfile],
        # CofferDamReinforcementProfile will be set for those without available measures.
        [],
        [],
    ]
    _strategy_locations = [
        _to_strategy_location(_idx, _rt_list)
        for _idx, _rt_list in enumerate(_initial_state_per_location)
    ]
    yield StrategyInput(
        strategy_locations=_strategy_locations,
        reinforcement_min_buffer=1,
        reinforcement_min_length=5,
    )


@pytest.fixture
def example_location_reinforcements_with_buffering(
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
