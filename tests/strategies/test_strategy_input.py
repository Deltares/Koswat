from koswat.strategies.strategy_input import StrategyInput


class TestStrategyInput:
    def test_initialize(self):
        # 1. Define test data
        _locations = []
        _min_buffer = 1
        _min_length = 2

        # 2. Run test.
        _input = StrategyInput(
            strategy_locations=_locations,
            reinforcement_min_buffer=_min_buffer,
            reinforcement_min_length=_min_length,
        )

        # 3. Verify expectations.
        assert isinstance(_input, StrategyInput)
        assert _input.strategy_locations == _locations
        assert _input.reinforcement_min_buffer == _min_buffer
        assert _input.reinforcement_min_length == _min_length
        assert _input.reinforcement_min_cluster == (2 * _min_buffer) + 1

    def test_given_nan_min_buffer_then_min_cluster_is_minus_one(self):
        # 1. Define test data.
        _input = StrategyInput(
            strategy_locations=[],
            reinforcement_min_buffer=float("nan"),
            reinforcement_min_length=float("nan"),
        )

        # 2. Verify expectations.
        assert _input.reinforcement_min_cluster == -1
