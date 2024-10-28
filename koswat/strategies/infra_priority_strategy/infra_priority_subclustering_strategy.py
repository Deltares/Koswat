from itertools import groupby
from typing import Iterator

import more_itertools

from koswat.strategies.infra_priority_strategy.infra_cluster import (
    InfraCluster,
    InfraClusterCollection,
)
from koswat.strategies.infra_priority_strategy.infra_priority_strategy import (
    InfraPriorityStrategy,
)
from koswat.strategies.order_strategy.order_strategy import OrderStrategy
from koswat.strategies.strategy_input import StrategyInput
from koswat.strategies.strategy_location_reinforcement import (
    StrategyLocationReinforcement,
)


class InfraPrioritySubclusteringStrategy(InfraPriorityStrategy):
    """
    KISSSSSSSSSSSSSSS
    """

    def _get_initial_clusters(
        self, strategy_input: StrategyInput
    ) -> list[InfraCluster]:
        _infra_cluster_list: list[InfraCluster] = []
        for _grouped_by, _grouping in groupby(
            OrderStrategy().apply_strategy(strategy_input),
            key=lambda x: x.selected_measure,
        ):
            _grouping_data = list(_grouping)
            if not _grouping_data:
                continue
            _cluster = InfraCluster(
                reinforcement_type=_grouped_by, cluster=_grouping_data
            )
            if any(_infra_cluster_list):
                # Add neighbors
                _cluster.left_neighbor = _infra_cluster_list[-1]
                _infra_cluster_list[-1].right_neighbor = _cluster
            _infra_cluster_list.append(_cluster)
        return _infra_cluster_list

    def _get_subclusters(
        self, infra_cluster: InfraCluster, min_length: float
    ) -> list[InfraClusterCollection]:
        if len(infra_cluster.cluster) < 2 * min_length:
            # If the cluster is not twice as big as the minimum
            # required length we know there is no possibility of
            # creating subclusters.
            return [
                InfraClusterCollection(
                    cluster_min_length=min_length, cluster_collection=[infra_cluster]
                )
            ]

        def windowed_cluster_to_icc(
            location_collection: list[StrategyLocationReinforcement],
        ) -> Iterator[InfraClusterCollection]:
            _icc = InfraClusterCollection(cluster_min_length=min_length)
            for _w_element in location_collection:
                if len(_w_element) > 0 or len(_w_element) < min_length:
                    # `window_complete` returns collections as:
                    # `[(), (A,B,C), (D,E,F)]`
                    # `[(A,B,C), (D,E,F), ()]`
                    # Which are valid except for the limit item.
                    continue
                _icc.add_cluster(
                    InfraCluster(
                        reinforcement_type=infra_cluster.reinforcement_type,
                        cluster=list(_w_element),
                    )
                )
            return _icc

        return list(
            filter(
                lambda x: x.valid_cluster(),
                map(
                    windowed_cluster_to_icc,
                    more_itertools.windowed_complete(infra_cluster.cluster, min_length),
                ),
            )
        )

    def apply_strategy(self, strategy_input: StrategyInput):
        # We override the strategy.
        _clustered_locations = []
        # 1. Run `OrderStrategy` to generate an initial cluster formation.
        for _infra_cluster in self._get_initial_clusters(strategy_input):
            # 2. Get common available measures for each cluster
            _subcluster_collection = self._get_subclusters(
                _infra_cluster, strategy_input.reinforcement_min_cluster
            )

            for _icc in _subcluster_collection:
                for _sc in _icc.cluster_collection:
                    _sc_costs = self._get_common_available_measures(_sc)
                    _sc.set_cheapest_common_available_measure(_sc_costs)

            # 3. Set the **cheapest** common available measure.
            _optimal_icc = min(_subcluster_collection, key=lambda icc: icc.total_cost)
            _clustered_locations.extend(_optimal_icc.clustered_locations)
        return _clustered_locations
