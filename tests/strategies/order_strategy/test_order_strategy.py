from koswat.dike_reinforcements.reinforcement_profile import (
    CofferdamReinforcementProfile,
    PipingWallReinforcementProfile,
    SoilReinforcementProfile,
    StabilityWallReinforcementProfile,
    VPSReinforcementProfile,
)
from koswat.strategies.order_strategy.order_strategy import OrderStrategy
from koswat.strategies.order_strategy.order_strategy_base import OrderStrategyBase
from koswat.strategies.strategy_input import StrategyInput
from koswat.strategies.strategy_location_reinforcement import (
    StrategyLocationReinforcement,
)


class TestOrderStrategy:
    _default_reinforcements = [
        SoilReinforcementProfile,
        VPSReinforcementProfile,
        PipingWallReinforcementProfile,
        StabilityWallReinforcementProfile,
        CofferdamReinforcementProfile,
    ]

    def test_initialize(self):
        # This test is just to ensure the design principle
        # of parameterless constructors is met.
        _strategy = OrderStrategy()
        assert isinstance(_strategy, OrderStrategy)

    def test_get_default_order_for_reinforcements(self):
        # 1. Define test data.
        _expected_result = self._default_reinforcements

        # 2. Run test.
        _result = OrderStrategy.get_default_order_for_reinforcements()

        # 3. Verify expectations
        assert _result == _expected_result

    def test_get_strategy_order_for_reinforcements(
        self,
        example_strategy_input: StrategyInput,
    ):
        # 1. Define test data.
        _expected_result = [SoilReinforcementProfile, CofferdamReinforcementProfile]
        _strategy = OrderStrategy()

        # 2. Run test.
        _reinforcements = _strategy.get_strategy_order_for_reinforcements(
            example_strategy_input
        )

        # 3. Verify expectations
        assert _reinforcements == _expected_result
        assert _reinforcements[-1] == CofferdamReinforcementProfile

    def test__get_strategy_reinforcements_given_example(
        self, example_strategy_input: StrategyInput
    ):
        # 1. Define test data.
        _default_order = OrderStrategy.get_default_order_for_reinforcements()
        assert _default_order[-1] == CofferdamReinforcementProfile

        # 2. Run test.
        _reinforcements = OrderStrategy.get_strategy_reinforcements(
            example_strategy_input.strategy_locations, _default_order
        )

        # 3. Verify expectations
        assert isinstance(_reinforcements, list)
        assert len(_reinforcements) == len(example_strategy_input.strategy_locations)

        def assert_subset_selected_measure(selected_measure: type, subset: list):
            assert all(_r.selected_measure == selected_measure for _r in subset)

        assert_subset_selected_measure(SoilReinforcementProfile, _reinforcements[:3])
        assert_subset_selected_measure(
            StabilityWallReinforcementProfile, _reinforcements[3:5]
        )
        assert_subset_selected_measure(SoilReinforcementProfile, _reinforcements[5:8])
        assert_subset_selected_measure(
            CofferdamReinforcementProfile, _reinforcements[8:]
        )

    def test__get_reinforcement_clusters_given_example(
        self,
        example_location_reinforcements_with_buffering: list[
            StrategyLocationReinforcement
        ],
    ):
        # 1. Define test data.
        class MockedStrategy(OrderStrategyBase):
            def __init__(self) -> None:
                self.reinforcement_order = (
                    OrderStrategy.get_default_order_for_reinforcements()
                )

            def apply(
                self, location_reinforcements: list[StrategyLocationReinforcement]
            ) -> None:
                pass

        _expected_clusters = [
            (0, example_location_reinforcements_with_buffering[:2]),
            (3, example_location_reinforcements_with_buffering[2:6]),
            (0, example_location_reinforcements_with_buffering[6:7]),
            (4, example_location_reinforcements_with_buffering[7:]),
        ]

        # 2. Run test.
        _result_clusters = MockedStrategy()._get_reinforcement_groupings(
            example_location_reinforcements_with_buffering
        )

        # 3. Verify expectations.
        assert _result_clusters == _expected_clusters

    def test_apply_strategy_given_example(self, example_strategy_input: StrategyInput):
        # 1. Define test data.
        assert isinstance(example_strategy_input, StrategyInput)

        # 2. Run test.
        _strategy_result = OrderStrategy().apply_strategy(example_strategy_input)

        # 3. Verify final expectations.
        assert isinstance(_strategy_result, list)
        assert len(_strategy_result) == len(example_strategy_input.strategy_locations)
        assert all(
            isinstance(_sr, StrategyLocationReinforcement) for _sr in _strategy_result
        )

        # Basically the same checks as in `test__apply_min_distance_given_example`.
        assert all(
            _sr.selected_measure == SoilReinforcementProfile
            for _sr in _strategy_result[0:2]
        )
        assert all(
            _sr.selected_measure == StabilityWallReinforcementProfile
            for _sr in _strategy_result[2:7]
        )
        assert all(
            _sr.selected_measure == CofferdamReinforcementProfile
            for _sr in _strategy_result[7:]
        )
