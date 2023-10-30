import pytest
from koswat.dike.surroundings.point.point_surroundings import PointSurroundings

from koswat.strategies.order_strategy.order_cluster import OrderCluster
from koswat.strategies.strategy_location_reinforcement import (
    StrategyLocationReinforcement,
)


class TestOrderCluster:
    @pytest.fixture
    def basic_order_cluster(self) -> OrderCluster:
        yield OrderCluster(reinforcement_idx=1, location_reinforcements=[])

    @pytest.mark.parametrize(
        "left_neighbor, right_neighbor",
        [
            pytest.param(False, False, id="No neighbors"),
            pytest.param(False, True, id="No left neighbor"),
            pytest.param(True, False, id="No right neighbor"),
        ],
    )
    def test_is_compliant_given_no_neighbor_returns_true(
        self,
        left_neighbor: bool,
        right_neighbor: bool,
        basic_order_cluster: OrderCluster,
    ):
        # 1. Define test data.
        if left_neighbor:
            basic_order_cluster.left_neighbor = "sth"
        if right_neighbor:
            basic_order_cluster.right_neighbor = "sth"

        assert not (
            basic_order_cluster.left_neighbor and basic_order_cluster.right_neighbor
        )

        # 2. Run test
        assert basic_order_cluster.is_compliant(
            basic_order_cluster.reinforcement_idx - 1,
            len(basic_order_cluster.location_reinforcements) - 1,
        )

    @pytest.fixture
    def order_cluster_with_neighbors(
        self, basic_order_cluster: OrderCluster
    ) -> OrderCluster:
        # Set locations.
        for _idx in range(0, 4):
            _dummy_location = StrategyLocationReinforcement(
                location=PointSurroundings(section="test", traject_order=_idx),
                selected_measure=[],
                available_measures=[],
            )
            basic_order_cluster.location_reinforcements.append(_dummy_location)

        # Set neighbors.
        _dummy_left = OrderCluster(
            reinforcement_idx=basic_order_cluster.reinforcement_idx + 1,
            location_reinforcements=[],
        )
        _dummy_right = OrderCluster(
            reinforcement_idx=_dummy_left.reinforcement_idx + 2,
            location_reinforcements=[],
        )

        # Just a triangle :)
        basic_order_cluster.left_neighbor = _dummy_left
        basic_order_cluster.right_neighbor = _dummy_right

        _dummy_left.right_neighbor = basic_order_cluster
        _dummy_left.left_neighbor = _dummy_right

        _dummy_right.left_neighbor = basic_order_cluster
        _dummy_right.right_neighbor = _dummy_left

        yield basic_order_cluster

    def test_is_compliant_given_enough_locations_return_true(
        self, order_cluster_with_neighbors: OrderCluster
    ):
        # 1. Define test data.
        _min_length = len(order_cluster_with_neighbors.location_reinforcements) - 1

        # 2. Run test.
        assert order_cluster_with_neighbors.is_compliant(_min_length, -1)

    def test_is_compliant_given_neighbors_but_invalid_length_and_reinforcement_returns_false(
        self,
        order_cluster_with_neighbors: OrderCluster,
    ):
        # 1. Define test data.
        _min_length = len(order_cluster_with_neighbors.location_reinforcements) + 1
        _strongest_idx = order_cluster_with_neighbors.reinforcement_idx + 1

        # 2. Run test.
        assert not order_cluster_with_neighbors.is_compliant(
            _min_length, _strongest_idx
        )

    def test_get_stronger_without_neighbors_returns_self(
        self, basic_order_cluster: OrderCluster
    ):
        # 1. Define test data.
        assert basic_order_cluster.left_neighbor is None
        assert basic_order_cluster.right_neighbor is None

        # 2. Run test.
        assert basic_order_cluster.get_stronger_cluster() == basic_order_cluster

    def test_get_stronger_with_neighbors_returns_min_of_them(
        self, order_cluster_with_neighbors: OrderCluster
    ):
        # 1. Define test data.
        assert isinstance(order_cluster_with_neighbors.left_neighbor, OrderCluster)
        assert isinstance(order_cluster_with_neighbors.right_neighbor, OrderCluster)
        assert (
            order_cluster_with_neighbors.left_neighbor.reinforcement_idx
            < order_cluster_with_neighbors.right_neighbor.reinforcement_idx
        )

        # 2. Verify expectations
        assert (
            order_cluster_with_neighbors.get_stronger_cluster()
            == order_cluster_with_neighbors.left_neighbor
        )

    def test_extend_cluster_updates_values_to_the_left(
        self, order_cluster_with_neighbors: OrderCluster
    ):
        # 1. Define test data.
        _selected_measure_value = "NotAMeasureDoesNotMatter"
        _merging_to = order_cluster_with_neighbors.left_neighbor
        _single_location = StrategyLocationReinforcement(
            location=PointSurroundings(),
            selected_measure=_selected_measure_value,
            available_measures=[],
        )
        _merging_to.location_reinforcements = [_single_location]

        # 2. Run test.
        order_cluster_with_neighbors.left_neighbor.extend_cluster(
            order_cluster_with_neighbors
        )

        # 3. Verify expectations
        assert all(
            lr.selected_measure == _selected_measure_value
            for lr in order_cluster_with_neighbors.location_reinforcements
        )
        assert _merging_to.right_neighbor == order_cluster_with_neighbors.right_neighbor
        assert _merging_to.location_reinforcements.index(_single_location) == 0
        assert (
            _merging_to.location_reinforcements[1:]
            == order_cluster_with_neighbors.location_reinforcements
        )

    def test_extend_cluster_updates_values_to_the_right(
        self, order_cluster_with_neighbors: OrderCluster
    ):
        # 1. Define test data.
        _selected_measure_value = "NotAMeasureDoesNotMatter"
        _merging_to = order_cluster_with_neighbors.right_neighbor
        _single_location = StrategyLocationReinforcement(
            location=PointSurroundings(),
            selected_measure=_selected_measure_value,
            available_measures=[],
        )
        _merging_to.location_reinforcements = [_single_location]

        # 2. Run test.
        order_cluster_with_neighbors.right_neighbor.extend_cluster(
            order_cluster_with_neighbors
        )

        # 3. Verify expectations
        assert all(
            lr.selected_measure == _selected_measure_value
            for lr in order_cluster_with_neighbors.location_reinforcements
        )
        assert _merging_to.left_neighbor == order_cluster_with_neighbors.left_neighbor
        assert (
            _merging_to.location_reinforcements.index(_single_location)
            == len(_merging_to.location_reinforcements) - 1
        )
        assert (
            _merging_to.location_reinforcements[:-1]
            == order_cluster_with_neighbors.location_reinforcements
        )

    def test_extend_cluster_given_unrelated_cluster_raises_error(
        self, order_cluster_with_neighbors: OrderCluster
    ):
        # 1. Define test data.
        _unrelated_cluster = OrderCluster(
            reinforcement_idx=42, location_reinforcements=[]
        )
        assert _unrelated_cluster.left_neighbor is None
        assert _unrelated_cluster.right_neighbor is None

        # 2. Run test.
        with pytest.raises(ValueError) as exc_err:
            _unrelated_cluster.extend_cluster(order_cluster_with_neighbors)

        # 3. Verify expectations.
        assert str(exc_err.value) == "Trying to extend cluster from an unrelated one."
