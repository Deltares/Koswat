"""
                    GNU GENERAL PUBLIC LICENSE
                      Version 3, 29 June 2007

    KOSWAT, from the dutch combination of words `Kosts-Wat` (what are the costs)
    Copyright (C) 2025 Stichting Deltares

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program.  If not, see <http://www.gnu.org/licenses/>.
"""

from __future__ import annotations

import logging
from dataclasses import dataclass

from koswat.strategies.strategy_location_reinforcement import (
    StrategyLocationReinforcement,
)
from koswat.strategies.strategy_step.strategy_step_enum import StrategyStepEnum


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
        """
        Gets the neighbor with the lowest reinforcement type value greater
        than the current cluster's value (`self.reinforcement_idx`).

        Returns:
            OrderCluster: Neighbor with a stronger `ReinforcementProfileProtocol`.
        """
        # DESIGN / THEORY decision:
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
        # We favor first towards the "next" cluster, in case both sides have the
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

    def extend_cluster(self, other: OrderCluster):
        """
        Extends the current cluster with the reinforcements
        (`list[StrategyLocationReinforcement]`) from another cluster.
        Modifies the `current_selected_measure` property of those measures being merged but it
        does not remove them from their source cluster.

        Args:
            other (OrderCluster): Cluster whose contents will be used to extend `self`.

        Raises:
            ValueError: When trying to extend from an unrelated cluster.
        """
        if self.left_neighbor != other and self.right_neighbor != other:
            logging.warning("Trying to extend cluster from an unrelated one.")

        if any(self.location_reinforcements):
            _new_profile_type = self.location_reinforcements[0].current_selected_measure
            for _lr in other.location_reinforcements:
                _lr.set_selected_measure(_new_profile_type, StrategyStepEnum.ORDERED)

        if self.left_neighbor == other:
            self.location_reinforcements = (
                other.location_reinforcements + self.location_reinforcements
            )
            self.left_neighbor = other.left_neighbor
        else:
            self.location_reinforcements = (
                self.location_reinforcements + other.location_reinforcements
            )
            self.right_neighbor = other.right_neighbor

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

        if (
            len(self.location_reinforcements) >= min_length
            or self.reinforcement_idx == strongest_reinforcement
        ):
            # It fulfills the required length,
            # or it is already the strongest reinforcement possible.
            return True

        # If there are no stronger neighbors,
        # it is also considered compliant (as an exception).
        return self.get_stronger_cluster() == self
