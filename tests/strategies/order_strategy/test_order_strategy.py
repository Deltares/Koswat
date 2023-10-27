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
from koswat.strategies.strategy_location_reinforcement import (
    StrategyLocationReinforcement,
)


class TestOrderStrategy:
    def test_initialize(self):
        # This test is just to ensure the design principle
        # of parameterless constructors is met.
        _strategy = OrderStrategy()
        assert isinstance(_strategy, OrderStrategy)
        assert len(_strategy._order_reinforcement) == 4

    @pytest.fixture
    def example_strategy_input(self) -> StrategyInput:
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

    def test_apply_strategy_given_valid_data(
        self, example_strategy_input: StrategyInput
    ):
        # 1. Define test data.
        assert isinstance(example_strategy_input, StrategyInput)
        _expected_cofferdam = 3

        # 2. Run test.
        _strategy_result = OrderStrategy().apply_strategy(example_strategy_input)

        # 3. Verify final expectations.
        assert isinstance(_strategy_result, list)
        assert len(_strategy_result) == len(
            example_strategy_input.locations_matrix.keys()
        )
        assert all(
            isinstance(_sr, StrategyLocationReinforcement) for _sr in _strategy_result
        )
        assert all(
            _sr.selected_measure == StabilityWallReinforcementProfile
            for _sr in _strategy_result[:-_expected_cofferdam]
        )
        assert all(
            _sr.selected_measure == CofferdamReinforcementProfile
            for _sr in _strategy_result[-_expected_cofferdam:]
        )
