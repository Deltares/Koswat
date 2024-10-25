from koswat.strategies.infra_priority_strategy.infra_priority_strategy import (
    InfraPriorityStrategy,
)


class InfraPrioritySubclusteringStrategy(InfraPriorityStrategy):
    def apply_strategy(self, strategy_input):
        # We override the strategy.
        return super().apply_strategy(strategy_input)
