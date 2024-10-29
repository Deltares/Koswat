from __future__ import annotations

from koswat.dike_reinforcements.reinforcement_profile.reinforcement_profile_protocol import (
    ReinforcementProfileProtocol,
)
from koswat.strategies.infra_priority_strategy.infra_cluster import InfraCluster


class InfraClusterOption:
    """
    Represents one set of (sub) clusters the strategy could select
    for costs optimization.
    """

    _cluster_collection: list[InfraCluster]
    _cluster_costs: list[dict[ReinforcementProfileProtocol, float]]
    _cluster_min_length: int

    def __init__(self, cluster_min_length: int):
        self._cluster_collection = []
        self._cluster_costs = []
        self._cluster_min_length = cluster_min_length

    @property
    def cluster_collection(self) -> list[InfraCluster]:
        """
        Read-only property to expose the stored subclusters.
        """
        return self._cluster_collection

    @property
    def cluster_costs(
        self,
    ) -> list[dict[ReinforcementProfileProtocol, float]]:
        """
        Read-only property to expose the stored costs.
        """
        return self._cluster_costs

    def add_cluster(self, infra_cluster: InfraCluster, cluster_costs: dict):
        """
        Adds the infra cluster into the collection as well as its reinforcement
        costs.

        Args:
            infra_cluster (InfraCluster): Cluster to add to this collection option.
            cluster_costs (dict): Reinforcement costs for the given cluster.
        """
        self._cluster_collection.append(infra_cluster)
        self._cluster_costs.append(cluster_costs)

    def valid_option(self) -> bool:
        """
        Validates the collection of clusters based on the
        required minimun length.

        Returns:
            bool: Validation result.
        """
        return any(self.cluster_collection) and all(
            len(_ic.cluster) >= self._cluster_min_length
            for _ic in self.cluster_collection
        )

    def set_cheapest_option(self):
        """
        Sets the subclusters defined in this option to their most optimal (cheapest)
        reinforcement possible.
        """
        for _cluster, _costs in zip(self._cluster_collection, self._cluster_costs):
            _cluster.set_cheapest_common_available_measure(_costs)
