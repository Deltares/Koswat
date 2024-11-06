from koswat.dike_reinforcements.reinforcement_profile.outside_slope.cofferdam_reinforcement_profile import (
    CofferdamReinforcementProfile,
)
from koswat.dike_reinforcements.reinforcement_profile.standard.soil_reinforcement_profile import (
    SoilReinforcementProfile,
)
from koswat.dike_reinforcements.reinforcement_profile.standard.stability_wall_reinforcement_profile import (
    StabilityWallReinforcementProfile,
)
from koswat.strategies.order_strategy.order_cluster import OrderCluster
from koswat.strategies.order_strategy.order_strategy import OrderStrategy
from koswat.strategies.order_strategy.order_strategy_base import OrderStrategyBase
from koswat.strategies.order_strategy.order_strategy_clustering import (
    OrderStrategyClustering,
)
from koswat.strategies.strategy_input import StrategyInput
from koswat.strategies.strategy_location_reinforcement import (
    StrategyLocationReinforcement,
)


class TestOrderStrategyClustering:
    def test_initialize(self):
        _strategy = OrderStrategyClustering()
        assert isinstance(_strategy, OrderStrategyClustering)
        assert isinstance(_strategy, OrderStrategyBase)

    def test_apply_given_example_docs(
        self,
        example_strategy_input: StrategyInput,
        example_location_reinforcements_with_buffering: list[
            StrategyLocationReinforcement
        ],
    ):
        # 1. Define test data.
        _strategy = OrderStrategyClustering()
        _strategy.reinforcement_min_length = (
            example_strategy_input.reinforcement_min_length
        )
        _strategy.reinforcement_order = (
            OrderStrategy.get_default_order_for_reinforcements()
        )

        # 2. Run test.
        _strategy.apply(example_location_reinforcements_with_buffering)

        # 3. Verify expectations.
        assert all(
            _sr.current_selected_measure == SoilReinforcementProfile
            for _sr in example_location_reinforcements_with_buffering[0:2]
        )
        assert all(
            _sr.current_selected_measure == StabilityWallReinforcementProfile
            for _sr in example_location_reinforcements_with_buffering[2:7]
        )
        assert all(
            _sr.current_selected_measure == CofferdamReinforcementProfile
            for _sr in example_location_reinforcements_with_buffering[7:]
        )

    def test_apply_given_cluster_with_lower_type(
        self,
        example_location_reinforcements_with_buffering: list[
            StrategyLocationReinforcement
        ],
    ):
        # 1. Define test data.
        _strategy = OrderStrategyClustering()
        _strategy.reinforcement_min_length = 2
        _strategy.reinforcement_order = (
            OrderStrategy.get_default_order_for_reinforcements()
        )

        _location_reinforcements = example_location_reinforcements_with_buffering

        # Set all locations to the lowest type:
        for location_reinforcement in _location_reinforcements:
            location_reinforcement.set_selected_measure(
                _strategy.reinforcement_order[0], None
            )

        # Create an isolated cluster in the middle.
        _mid_cluster = len(_location_reinforcements) // 2
        _location_reinforcements[_mid_cluster].set_selected_measure(
            _strategy.reinforcement_order[1], None
        )

        # 2. Run test.
        _strategy.apply(example_location_reinforcements_with_buffering)

        # 3. Verify expectations.
        assert (
            _location_reinforcements[_mid_cluster].current_selected_measure
            == _strategy.reinforcement_order[1]
        )
        assert all(
            _sr.current_selected_measure == _strategy.reinforcement_order[0]
            for _sr in _location_reinforcements[0:_mid_cluster]
            + _location_reinforcements[_mid_cluster + 1 :]
        )

    def test__get_reinforcement_order_clusters(
        self,
        example_strategy_input: StrategyInput,
        example_location_reinforcements_with_buffering: list[
            StrategyLocationReinforcement
        ],
    ):
        # 1. Define test data.
        _strategy = OrderStrategyClustering()
        _strategy.reinforcement_min_length = (
            example_strategy_input.reinforcement_min_length
        )
        _strategy.reinforcement_order = (
            OrderStrategy.get_default_order_for_reinforcements()
        )

        # 2. Run test.
        _order_clusters = _strategy._get_reinforcement_order_clusters(
            example_location_reinforcements_with_buffering
        )

        # 3. Verify expectations.
        assert len(_order_clusters) == 4

        def assert_valid_cluster(cluster: OrderCluster) -> bool:
            assert isinstance(cluster, OrderCluster)
            assert any(cluster.location_reinforcements)
            assert isinstance(cluster.reinforcement_idx, int)
            assert isinstance(cluster.left_neighbor, OrderCluster) or isinstance(
                cluster.right_neighbor, OrderCluster
            )

        for _cluster in _order_clusters:
            assert_valid_cluster(_cluster)
