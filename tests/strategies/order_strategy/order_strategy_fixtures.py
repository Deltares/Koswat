import pytest
from koswat.dike.surroundings.point.point_surroundings import PointSurroundings
from koswat.dike_reinforcements.reinforcement_profile.standard.soil_reinforcement_profile import SoilReinforcementProfile
from koswat.dike_reinforcements.reinforcement_profile.standard.stability_wall_reinforcement_profile import StabilityWallReinforcementProfile

from koswat.strategies.strategy_input import StrategyInput

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