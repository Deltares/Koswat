from koswat.strategies.infra_priority_strategy.infra_priority_strategy import (
    InfraPriorityStrategy,
)
from koswat.strategies.strategy_protocol import StrategyProtocol


class TestInfraPriorityStrategy:
    def test_initialize(self):
        # 1. Define and run test data.
        _strategy = InfraPriorityStrategy()

        # 2. Verify expectations.
        assert isinstance(_strategy, InfraPriorityStrategy)
        assert isinstance(_strategy, StrategyProtocol)
