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
    reinforcement_order: list[type[ReinforcementProfileProtocol]]
    reinforcement_min_length: float

    @classmethod
    def with_strategy(
        cls,
        reinforcement_order: list[type[ReinforcementProfileProtocol]],
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

    def _get_non_compliant_clusters(
        self, target_reinforcement_idx: int, available_clusters: list[OrderCluster]
    ) -> list[OrderCluster]:
        return list(
            filter(
                lambda x: not x.is_compliant(
                    self.reinforcement_min_length, self.reinforcement_order[-1]
                )
                and x.reinforcement_idx == target_reinforcement_idx,
                available_clusters,
            )
        )

    def apply(
        self, location_reinforcements: list[StrategyLocationReinforcement]
    ) -> None:
        _available_clusters = self._get_reinforcement_order_clusters(
            location_reinforcements
        )
        _reinforcements_order_max_idx = len(self.reinforcement_order)
        for _target_idx, _reinforcement_type in enumerate(
            self.reinforcement_order[:-1]
        ):
            _non_compliant_clusters = self._get_non_compliant_clusters(
                _target_idx, _available_clusters
            )
            logging.info(
                "Non-compliant clusters found for {}: {}".format(
                    _reinforcement_type.output_name, len(_non_compliant_clusters)
                )
            )
            for _cluster in _non_compliant_clusters:
                if _cluster.is_compliant(
                    self.reinforcement_min_length, _reinforcements_order_max_idx
                ):
                    continue
                _stronger_cluster = _cluster.get_stronger_cluster()
                # Update selected measures for locations in this cluster.
                _stronger_cluster.extend_cluster(_cluster)
                _available_clusters.pop(_available_clusters.index(_cluster))
