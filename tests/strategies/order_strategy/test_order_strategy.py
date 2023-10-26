from koswat.strategies.order_strategy.order_strategy import OrderStrategy
from koswat.strategies.strategy_input import StrategyInput


class TestOrderStrategy:
    def test_initialize(self):
        # This test is just to ensure the design principle
        # of parameterless constructors is met.
        _strategy = OrderStrategy()
        assert isinstance(_strategy, OrderStrategy)

    def test_from_strategy_input_sets_values(self):
        # 1. Define test data.
        _matrix = dict()
        _structure_buffer = 50
        _structure_space = 10
        _strategy_input = StrategyInput(
            locations_matrix=_matrix,
            structure_buffer=_structure_buffer,
            min_space_between_structures=_structure_space
        )
        
        # 2. Run test.
        _strategy = OrderStrategy.from_strategy_input(_strategy_input)

        # 3. Verify final expectations.
        assert isinstance(_strategy, OrderStrategy)
        
        # This is not required because they are internal properties.
        assert isinstance(_strategy._order_reinforcement, list)
        assert any(_strategy._order_reinforcement)
        assert _strategy._location_matrix == _matrix
        assert _strategy._structure_buffer == _structure_buffer
        assert _strategy._min_space_between_structures == _structure_space