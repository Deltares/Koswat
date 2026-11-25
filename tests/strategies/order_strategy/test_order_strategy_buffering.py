from koswat.strategies.order_strategy.order_strategy import OrderStrategy
from koswat.strategies.order_strategy.order_strategy_base import OrderStrategyBase
from koswat.strategies.order_strategy.order_strategy_buffering import (
    OrderStrategyBuffering,
)
from koswat.strategies.strategy_input import StrategyInput
from koswat.strategies.strategy_reinforcement_input.strategy_reinforcement_input_protocol import (
    StrategyReinforcementInputProtocol,
)


class TestOrderStrategyBuffering:
    def test_initialize(self):
        _strategy = OrderStrategyBuffering(
            reinforcement_order=[],
            reinforcement_min_buffer=float("nan"),
        )
        assert isinstance(_strategy, OrderStrategyBuffering)
        assert isinstance(_strategy, OrderStrategyBase)

    def test_apply_given_docs_example(
        self,
        example_strategy_input: StrategyInput,
        example_default_order: list[type[StrategyReinforcementInputProtocol]],
    ):
        # 1. Define test data.
        _reinforcements = OrderStrategy.get_strategy_reinforcements(
            example_strategy_input.strategy_locations,
            example_default_order,
        )
        _strategy = OrderStrategyBuffering(
            reinforcement_order=example_default_order,
            reinforcement_min_buffer=example_strategy_input.reinforcement_min_buffer,
        )

        _expected_result_idx = [0, 0, 4, 4, 4, 4, 0, 5, 5, 5]
        _expected_result = list(
            map(lambda x: example_default_order[x], _expected_result_idx)
        )

        # 2. Run test.
        _strategy.apply(_reinforcements)

        # 3. Verify expectations.
        assert all(
            _r.current_selected_measure == _expected_result[_r_idx]
            for _r_idx, _r in enumerate(_reinforcements)
        )

    def test__get_buffer_mask_given_docs_example(
        self,
        example_strategy_input: StrategyInput,
        example_default_order: list[type[StrategyReinforcementInputProtocol]],
    ):
        # 1. Define test data.
        _reinforcements = OrderStrategy.get_strategy_reinforcements(
            example_strategy_input.strategy_locations,
            example_default_order,
        )
        _strategy = OrderStrategyBuffering(
            reinforcement_order=example_default_order,
            reinforcement_min_buffer=example_strategy_input.reinforcement_min_buffer,
        )

        # 2. Run test.
        _mask_result = _strategy._get_buffer_mask(_reinforcements)

        # 3. Verify expectations.
        assert _mask_result == [0, 0, 4, 4, 4, 4, 0, 5, 5, 5]

    def test__get_modified_example_last_location_gets_buffered(
        self,
        example_strategy_input: StrategyInput,
        example_default_order: list[type[StrategyReinforcementInputProtocol]],
    ):
        """
        This test fixes the problem related to Koswat #220.
        """
        # 1. Define test data.
        _reinforcements = OrderStrategy.get_strategy_reinforcements(
            example_strategy_input.strategy_locations,
            example_default_order,
        )[:6]
        _strategy = OrderStrategyBuffering(
            reinforcement_order=example_default_order,
            reinforcement_min_buffer=3,
        )

        # 2. Run test.
        _mask_result = _strategy._get_buffer_mask(_reinforcements)

        # 3. Verify expectations.
        assert _mask_result == [4, 4, 4, 4, 4, 4]
