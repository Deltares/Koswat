from __future__ import annotations

from dataclasses import dataclass

from koswat.strategies.strategy_location_reinforcement import (
    StrategyLocationReinforcement,
)


@dataclass
class OrderCluster:
    reinforcement_idx: int
    location_reinforcements: list[StrategyLocationReinforcement]

    def is_compliant(self, min_length: float, strongest_reinforcement: int) -> bool:
        """
        Checks whether this `OrderCluster` instance is compliant with the `OrderStrategy`
        rules for a reinforcement cluster.

        Args:
            min_length (float): Minimal length a reinforcement measure is required
            for a cluster.
            strongest_reinforcement (int): What is the reinforcement index which cannot
            be futher 'strengthen'.

        Returns:
            bool: if length is appropiate or this cluster is an exception instead.

        """
        if self.reinforcement_idx == strongest_reinforcement:
            # It is already the strongest reinforcement, it cannot be further strengthen.
            return True
        return len(self.location_reinforcements) >= min_length


@dataclass
class OrderClusterWithNeighbors:
    cluster: OrderCluster
    left_neighbor: OrderCluster | None = None
    right_neighbor: OrderCluster | None = None

    def is_compliant(self, min_length: float, strongest_reinforcement: int) -> bool:
        """
        Checks whether this `OrderCluster` instance is compliant within a cluster group.

        Args:
            min_length (float): Minimal length a reinforcement measure is required
            for a cluster.
            strongest_reinforcement (int): What is the reinforcement index which cannot
            be futher 'strengthen'.

        Returns:
            bool: if the cluster is compliant within its neighbors context.
        """
        if not self.left_neighbor or not self.right_neighbor:
            # It is a bordering cluster, it is always compliant.
            return True
        return self.cluster.is_compliant(min_length, strongest_reinforcement)
