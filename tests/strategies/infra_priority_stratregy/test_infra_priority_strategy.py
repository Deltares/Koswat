from koswat.dike_reinforcements.reinforcement_profile.outside_slope.cofferdam_reinforcement_profile import (
    CofferdamReinforcementProfile,
)
from koswat.dike_reinforcements.reinforcement_profile.standard.piping_wall_reinforcement_profile import (
    PipingWallReinforcementProfile,
)
from koswat.dike_reinforcements.reinforcement_profile.standard.stability_wall_reinforcement_profile import (
    StabilityWallReinforcementProfile,
)
from koswat.strategies.infra_priority_strategy.infra_priority_strategy import (
    InfraPriorityStrategy,
)
from koswat.strategies.infra_priority_strategy.infra_priority_subclustering_strategy import (
    InfraPrioritySubclusteringStrategy,
)
from koswat.strategies.strategy_input import StrategyInput
from koswat.strategies.strategy_location_reinforcement import (
    StrategyLocationReinforcement,
)
from koswat.strategies.strategy_protocol import StrategyProtocol


class TestInfraPriorityStrategy:
    def test_initialize(self):
        # 1. Define and run test data.
        _strategy = InfraPriorityStrategy()

        # 2. Verify expectations.
        assert isinstance(_strategy, InfraPriorityStrategy)
        assert isinstance(_strategy, StrategyProtocol)

    def test_given_example_when_apply_strategy_then_gets_new_ones(
        self, example_strategy_input: StrategyInput
    ):
        # 1. Define test data.
        assert isinstance(example_strategy_input, StrategyInput)

        # 2. Run test.
        _strategy_result = InfraPriorityStrategy().apply_strategy(
            example_strategy_input
        )

        # 3. Verify final expectations.
        assert isinstance(_strategy_result, list)
        assert len(_strategy_result) == len(example_strategy_input.strategy_locations)
        assert all(
            isinstance(_sr, StrategyLocationReinforcement) for _sr in _strategy_result
        )

        # Basically the same checks as in `test__apply_min_distance_given_example`.
        assert all(
            _sr.selected_measure == PipingWallReinforcementProfile
            for _sr in _strategy_result[0:2]
        )
        assert all(
            _sr.selected_measure == CofferdamReinforcementProfile
            for _sr in _strategy_result[2:]
        )


class TestInfraPrioritySubsclusteringStrategy:
    def test_with_subclusters(self, example_subclustering: StrategyInput):
        # 1. Define test data.
        assert isinstance(example_subclustering, StrategyInput)

        # 2. Run test.
        _strategy_result = InfraPrioritySubclusteringStrategy().apply_strategy(
            example_subclustering
        )

        # 3. Verify final expectations.
        assert isinstance(_strategy_result, list)
        assert len(_strategy_result) == len(example_subclustering.strategy_locations)
        assert all(
            isinstance(_sr, StrategyLocationReinforcement) for _sr in _strategy_result
        )

        # Basically the same checks as in `test__apply_min_distance_given_example`.
        assert all(
            _sr.selected_measure == PipingWallReinforcementProfile
            for _sr in _strategy_result[0:2]
        )
        assert all(
            _sr.selected_measure == StabilityWallReinforcementProfile
            for _sr in _strategy_result[2:5]
        )
        assert all(
            _sr.selected_measure == CofferdamReinforcementProfile
            for _sr in _strategy_result[5:]
        )
