from __future__ import annotations

from dataclasses import dataclass, field
from itertools import chain

from koswat.strategies.infra_priority_strategy.infra_cluster import InfraCluster
from koswat.strategies.strategy_location_reinforcement import (
    StrategyLocationReinforcement,
)


@dataclass
class InfraClusterCollection:
    cluster_min_length: int
    cluster_collection: list[InfraCluster] = field(default_factory=lambda: [])

    @property
    def total_cost(self) -> float:
        """
        The total (current cost) of this cluster.

        Returns:
            float: The total cost.
        """
        return sum(c.current_cost for c in self.cluster_collection)

    @property
    def clustered_locations(self) -> list[StrategyLocationReinforcement]:
        """
        Returned all the clustered locations sparsed throughout
        the different subclusters.

        Returns:
            list[StrategyLocationReinforcement]: All the available locations.
        """
        return list(chain(*map(lambda x: x.cluster, self.cluster_collection)))

    def valid_cluster(self) -> bool:
        """
        Validates the collection of clusters based on the
        required minimun length.

        Returns:
            bool: Validation result.
        """
        return any(self.cluster_collection) and all(
            len(_ic.cluster) >= self.cluster_min_length
            for _ic in self.cluster_collection
        )

    def add_cluster(self, new_subcluster: InfraCluster) -> None:
        """
        Adds a new cluster (`InfraCluster`) to the current collection
        and corrects the neighbor properties to the new and existing
        clusters.

        Args:
            new_subcluster (InfraCluster): The cluster to add to this collection.
        """
        if any(self.cluster_collection):
            new_subcluster.left_neighbor = self.cluster_collection[-1]
            self.cluster_collection[-1].right_neighbor = new_subcluster
        self.cluster_collection.append(new_subcluster)
