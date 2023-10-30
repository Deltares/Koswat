from __future__ import annotations

from dataclasses import dataclass
from koswat.strategies.strategy_location_reinforcement import (
    StrategyLocationReinforcement,
)


@dataclass
class OrderCluster:
    reinforcement_idx: int
    location_reinforcements: list[StrategyLocationReinforcement]
    left_neighbor: OrderCluster | None = None
    right_neighbor: OrderCluster | None = None

    def __hash__(self) -> int:
        return hash(
            (
                self.reinforcement_idx,
                *[lr.location for lr in self.location_reinforcements],
            )
        )

    def get_stronger_cluster(self) -> OrderCluster:
        # DESIGN / THEORY decission:
        # We ensure no construction is replaced by a "lower" type.
        # This means a "short" `StabilityWallReinforcementProfile` won't be
        # replaced by a `SoilReinforcementProfile` and so on.

        _default_value = self.reinforcement_idx

        def valid_neighbor(neighbor_cluster: OrderCluster | None) -> bool:
            return (
                isinstance(neighbor_cluster, OrderCluster)
                and neighbor_cluster.reinforcement_idx > _default_value
            )

        # Selection criteria:
        # We merge first towards the "next" cluster, in case both sides have the
        # same type of reinforcement, to prevent it from being too short as we
        # assume clusters are being checked "left" to "right".

        return min(
            filter(
                valid_neighbor,
                [self.right_neighbor, self.left_neighbor],
            ),
            key=lambda x: x.reinforcement_idx,
            default=self,
        )

    def merge_cluster(self, other: OrderCluster):
        _new_profile_type = self.location_reinforcements[0].selected_measure
        for _lr in other.location_reinforcements:
            _lr.selected_measure = _new_profile_type

        if self.left_neighbor == other:
            self.location_reinforcements = (
                other.location_reinforcements + self.location_reinforcements
            )
            self.left_neighbor = other.left_neighbor
        else:
            self.location_reinforcements = (
                self.location_reinforcements + other.location_reinforcements
            )
            self.right_neighbor = other.left_neighbor

    def is_compliant(self, min_length: float, strongest_reinforcement: int) -> bool:
        """
        Checks whether this `OrderCluster` instance is compliant within a cluster group.
        This method does not check for exceptions, such as, the cluster's neighbors are
        of lower strength than the current.

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

        # It fulfills the required length,
        # or it is already the strongest reinforcement possible.
        return (
            len(self.location_reinforcements) >= min_length
            or self.reinforcement_idx == strongest_reinforcement
        )
