from koswat.strategies.order_strategy.order_strategy import OrderStrategy
from koswat.strategies.order_strategy.order_strategy_base import OrderStrategyBase
from koswat.strategies.order_strategy.order_strategy_buffering import (
    OrderStrategyBuffering,
)
from koswat.strategies.strategy_input import StrategyInput
from tests.strategies.order_strategy.order_strategy_fixtures import (  # Don't remove
    example_strategy_input,
)


class TestOrderStrategyBuffering:
    def test_initialize(self):
        _strategy = OrderStrategyBuffering()
        assert isinstance(_strategy, OrderStrategyBuffering)
        assert isinstance(_strategy, OrderStrategyBase)

    def test_apply_given_docs_example(self, example_strategy_input: StrategyInput):
        # 1. Define test data.
        _reinforcement_order = OrderStrategy.get_default_order_for_reinforcements()
        _reinforcements = OrderStrategy.get_strategy_reinforcements(
            example_strategy_input.locations_matrix,
            _reinforcement_order,
        )
        _strategy = OrderStrategyBuffering()
        _strategy.reinforcement_order = _reinforcement_order
        _strategy.reinforcement_min_buffer = (
            example_strategy_input.reinforcement_min_buffer
        )
        _expected_result_idx = [0, 0, 3, 3, 3, 3, 0, 4, 4, 4]
        _expected_result = list(
            map(lambda x: _reinforcement_order[x], _expected_result_idx)
        )

        # 2. Run test.
        _strategy.apply(_reinforcements)

        # 3. Verify expectations.
        assert all(
            _r.selected_measure == _expected_result[_r_idx]
            for _r_idx, _r in enumerate(_reinforcements)
        )

    def test__get_buffer_mask_given_docs_example(
        self, example_strategy_input: StrategyInput
    ):
        # 1. Define test data.
        _order_reinforcement = OrderStrategy.get_default_order_for_reinforcements()
        _reinforcements = OrderStrategy.get_strategy_reinforcements(
            example_strategy_input.locations_matrix,
            _order_reinforcement,
        )
        _strategy = OrderStrategyBuffering()
        _strategy.reinforcement_order = _order_reinforcement
        _strategy.reinforcement_min_buffer = (
            example_strategy_input.reinforcement_min_buffer
        )

        # 2. Run test.
        _mask_result = _strategy._get_buffer_mask(_reinforcements)

        # 3. Verify expectations.
        assert _mask_result == [0, 0, 3, 3, 3, 3, 0, 4, 4, 4]
