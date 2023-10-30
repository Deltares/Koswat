import pytest
from koswat.dike.surroundings.point.point_surroundings import PointSurroundings
from koswat.dike_reinforcements.reinforcement_profile.standard.soil_reinforcement_profile import (
    SoilReinforcementProfile,
)
from koswat.dike_reinforcements.reinforcement_profile.standard.stability_wall_reinforcement_profile import (
    StabilityWallReinforcementProfile,
)
from koswat.strategies.order_strategy.order_strategy import OrderStrategy

from koswat.strategies.strategy_input import StrategyInput
from koswat.strategies.strategy_location_reinforcement import (
    StrategyLocationReinforcement,
)


@pytest.fixture
def example_strategy_input() -> StrategyInput:
    # This is the data defined in the docs\reference\koswat_strategies.md
    # as examples. DON'T MODIFY IT!
    _matrix = {
        PointSurroundings(traject_order=0): [SoilReinforcementProfile],
        PointSurroundings(traject_order=1): [SoilReinforcementProfile],
        PointSurroundings(traject_order=2): [SoilReinforcementProfile],
        PointSurroundings(traject_order=3): [StabilityWallReinforcementProfile],
        PointSurroundings(traject_order=4): [StabilityWallReinforcementProfile],
        PointSurroundings(traject_order=5): [SoilReinforcementProfile],
        PointSurroundings(traject_order=6): [SoilReinforcementProfile],
        PointSurroundings(traject_order=7): [SoilReinforcementProfile],
        # CofferDamReinforcementProfile will be set for those without available measures.
        PointSurroundings(traject_order=8): [],
        PointSurroundings(traject_order=9): [],
    }
    yield StrategyInput(
        locations_matrix=_matrix, structure_min_buffer=1, structure_min_length=5
    )


@pytest.fixture
def example_location_reinforcements_with_buffering(
    example_strategy_input: StrategyInput,
) -> list[StrategyLocationReinforcement]:
    _result_after_buffering_idx = [0, 0, 2, 2, 2, 2, 0, 3, 3, 3]
    _measure_order = OrderStrategy.get_default_order_for_reinforcements()
    _location_reinforcements = []
    for _idx, _location in enumerate(example_strategy_input.locations_matrix.keys()):
        _measure_idx = _result_after_buffering_idx[_idx]
        _location_reinforcements.append(
            StrategyLocationReinforcement(
                location=_location,
                selected_measure=_measure_order[_measure_idx],
                available_measures=[],
            )
        )

    yield _location_reinforcements
