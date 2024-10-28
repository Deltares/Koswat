from __future__ import annotations

from dataclasses import dataclass, field
from typing import Iterator

from more_itertools import windowed_complete

from koswat.dike_reinforcements.reinforcement_profile.reinforcement_profile_protocol import (
    ReinforcementProfileProtocol,
)
from koswat.strategies.strategy_location_reinforcement import (
    StrategyLocationReinforcement,
)


@dataclass
class InfraCluster:
    reinforcement_type: type[ReinforcementProfileProtocol]
    cluster: list[StrategyLocationReinforcement] = field(default_factory=lambda: [])

    @property
    def current_cost(self) -> float:
        """
        Calculates the cost of applying the `reinforcement_type` to
        all locations present in the `cluster`.

        Returns:
            float: The total (current) cost of this cluster.
        """
        return sum(_c.current_cost for _c in self.cluster)

    def set_cheapest_common_available_measure(
        self,
        measure_costs: dict[type[ReinforcementProfileProtocol]],
    ) -> None:
        """
        Updates all the location reinforcements with the cheapest reinforcement type
        from the `measure_costs`.

        Args:
            measure_costs (dict[type[ReinforcementProfileProtocol]]):
                dictionary with the total costs per reinforcement type.
        """
        _selection = min(
            measure_costs,
            key=measure_costs.get,
        )

        if _selection != self.reinforcement_type:
            self.reinforcement_type = _selection
            for _cd in self.cluster:
                _cd.selected_measure = _selection

    def generate_subcluster_options(self, min_length: int) -> list[list[InfraCluster]]:
        """
        Generates all possible combinations of (sub) clusters based on the locations
        of this cluster. These are also referred as "options".

        Args:
            min_length (int): Minimun length for a cluster to be valid.

        Returns:
            list[list[InfraCluster]]: Collection of "options" with valid length.
        """

        def valid_cluster(infra_cluster: InfraCluster) -> bool:
            if not infra_cluster:
                return False
            return len(infra_cluster.cluster) >= min_length

        def valid_cluster_collection(cluster_collection: list[InfraCluster]) -> bool:
            if not cluster_collection:
                return False
            return all(map(valid_cluster, cluster_collection))

        if not valid_cluster(self) or len(self.cluster) < 2 * (min_length - 1):
            # If the cluster is not twice as big as the minimum
            # required length we know there is no possibility of
            # creating subclusters.
            return [[self]]

        def windowed_cluster_to_icc(
            location_collection: list[StrategyLocationReinforcement],
        ) -> Iterator[list[InfraCluster]]:
            _icc = []
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
                    _icc.clear()
                    break
                _icc.append(
                    InfraCluster(
                        reinforcement_type=self.reinforcement_type,
                        cluster=list(_w_element),
                    )
                )
            return _icc

        _valid_options = list(
            filter(
                valid_cluster_collection,
                map(
                    windowed_cluster_to_icc,
                    windowed_complete(self.cluster, min_length),
                ),
            )
        )

        if not _valid_options:
            # If no valid options were found, then just use the original state.
            return [[self]]

        return _valid_options
