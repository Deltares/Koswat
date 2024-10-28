from typing import Iterator

import more_itertools

from koswat.strategies.infra_priority_strategy.infra_cluster import InfraCluster
from koswat.strategies.infra_priority_strategy.infra_cluster_collection import (
    InfraClusterCollection,
)
from koswat.strategies.infra_priority_strategy.infra_priority_strategy import (
    InfraPriorityStrategy,
)
from koswat.strategies.strategy_input import StrategyInput
from koswat.strategies.strategy_location_reinforcement import (
    StrategyLocationReinforcement,
)


class InfraPrioritySubclusteringStrategy(InfraPriorityStrategy):
    def _get_subclusters(
        self, infra_cluster: InfraCluster, min_length: int
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
                if not _w_element:
                    # `window_complete` returns collections as:
                    # `[(), (A,B,C), (D,E,F)]`
                    # `[(A,B,C), (D,E,F), ()]`
                    # Which are valid except for the limit item.
                    continue
                if len(_w_element) < min_length:
                    # There is no need to check further,
                    # this cluster will result as not valid.
                    _icc.cluster_collection.clear()
                    break
                _icc.cluster_collection.append(
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

    def _set_cheapest_measure_per_cluster(
        self, infra_cluster, strategy_input: StrategyInput
    ):
        # 2. Get common available measures for each cluster
        _subcluster_collection = self._get_subclusters(
            infra_cluster, strategy_input.reinforcement_min_cluster
        )

        _min_costs = infra_cluster.current_cost
        _selected_cluster_collection_costs = None
        for _icc in _subcluster_collection:
            _icc_costs = 0
            _icc_cam_costs = []
            for _sc in _icc.cluster_collection:
                _icc_cam_costs.append(self.get_common_available_measures(_sc))
                _icc_costs += min(_icc_cam_costs[-1].values())
                if _icc_costs > _min_costs:
                    # No need to check further, it is more expensive already.
                    break
            if _icc_costs < _min_costs:
                # Replace cluster collection with minimal costs.
                _min_costs = _icc_costs
                _selected_cluster_collection_costs = list(
                    zip(_icc.cluster_collection, _icc_cam_costs)
                )

        # 3. Set the **cheapest** common available measure.
        if _selected_cluster_collection_costs:
            # Do nothing, we did not improve the cluster.
            for _sc, _costs in _selected_cluster_collection_costs:
                _sc.set_cheapest_common_available_measure(_costs)
