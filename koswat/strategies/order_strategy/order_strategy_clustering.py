import logging
from koswat.dike_reinforcements.reinforcement_profile.reinforcement_profile_protocol import (
    ReinforcementProfileProtocol,
)
from koswat.strategies.order_strategy.order_cluster import OrderCluster
from koswat.strategies.order_strategy.order_strategy_base import OrderStrategyBase
from koswat.strategies.strategy_location_reinforcement import (
    StrategyLocationReinforcement,
)


class OrderStrategyClustering(OrderStrategyBase):
    reinforcement_order: list[ReinforcementProfileProtocol]
    reinforcement_min_length: float

    @classmethod
    def with_strategy(
        cls,
        reinforcement_order: list[ReinforcementProfileProtocol],
        reinforcement_min_length: float,
    ):
        _this = cls()
        _this.reinforcement_order = reinforcement_order
        _this.reinforcement_min_length = reinforcement_min_length
        return _this

    def _get_reinforcement_order_clusters(
        self,
        location_reinforcements: list[StrategyLocationReinforcement],
    ) -> list[OrderCluster]:
        _added_clusters = []
        for _cluster in self._get_reinforcement_groupings(location_reinforcements):
            _last_added = OrderCluster(
                reinforcement_idx=_cluster[0],
                location_reinforcements=_cluster[1],
                left_neighbor=_added_clusters[-1] if any(_added_clusters) else None,
            )
            if isinstance(_last_added.left_neighbor, OrderCluster):
                _last_added.left_neighbor.right_neighbor = _last_added
            _added_clusters.append(_last_added)
        return _added_clusters

    def apply(
        self, location_reinforcements: list[StrategyLocationReinforcement]
    ) -> None:
        _available_clusters = self._get_reinforcement_order_clusters(
            location_reinforcements
        )
        _reinforcements_order_max_idx = len(self.reinforcement_order)
        for _target_reinforcement_idx in range(0, _reinforcements_order_max_idx - 1):
            _target_non_compliant_clusters = list(
                filter(
                    lambda x: not x.is_compliant(
                        self.reinforcement_min_length, self.reinforcement_order[-1]
                    )
                    and x.reinforcement_idx == _target_reinforcement_idx,
                    _available_clusters,
                )
            )
            if not any(_target_non_compliant_clusters):
                continue

            for _cluster in _target_non_compliant_clusters:
                if _cluster.is_compliant(
                    self.reinforcement_min_length, _reinforcements_order_max_idx
                ):
                    continue

                _stronger_cluster = _cluster.get_stronger_cluster()
                if _stronger_cluster == _cluster:
                    logging.warning(
                        "Cluster for {} not merged despite length at traject order {} - {}, as both sides ({}, {}) are inferior reinforcement types.".format(
                            self.reinforcement_order[_cluster.reinforcement_idx],
                            _cluster.location_reinforcements[0].location.traject_order,
                            _cluster.location_reinforcements[-1].location.traject_order,
                            self.reinforcement_order[
                                _cluster.left_neighbor.reinforcement_idx
                            ],
                            self.reinforcement_order[
                                _cluster.right_neighbor.reinforcement_idx
                            ],
                        )
                    )
                    continue
                # Update selected measures for locations in this cluster.
                _stronger_cluster.extend_cluster(_cluster)
                _available_clusters.pop(_available_clusters.index(_cluster))
