from koswat.strategies.order_strategy.order_strategy import OrderStrategy
from koswat.strategies.strategy_input import StrategyInput
from koswat.strategies.strategy_location_reinforcement import (
    StrategyLocationReinforcement,
)
from koswat.strategies.strategy_protocol import StrategyProtocol


class InfraPriorityStrategy(StrategyProtocol):
    def apply_strategy(
        self, strategy_input: StrategyInput
    ) -> list[StrategyLocationReinforcement]:
        # First apply `OrderStrategy` to generate an initial cluster formation.
        _initial_clusters = OrderStrategy().apply_strategy(strategy_input)

        return _initial_clusters
