from __future__ import annotations

from collections import defaultdict
from itertools import groupby

from koswat.dike_reinforcements.reinforcement_profile.reinforcement_profile_protocol import (
    ReinforcementProfileProtocol,
)
from koswat.strategies.infra_priority_strategy.infra_cluster import InfraCluster
from koswat.strategies.order_strategy.order_strategy import OrderStrategy
from koswat.strategies.strategy_input import StrategyInput
from koswat.strategies.strategy_location_reinforcement import (
    StrategyLocationReinforcement,
)
from koswat.strategies.strategy_protocol import StrategyProtocol


class InfraPriorityStrategy(StrategyProtocol):
    """
    This strategy works under the assumption that
    `StrategyLocationReinforcement.available_measures`
    ARE NOT ordered by "compatibility".
    Thus we need to check first which are the compatible reinforcements
    per cluster.
    """

    @staticmethod
    def get_common_available_measures(
        infra_cluster: InfraCluster,
    ) -> dict[type[ReinforcementProfileProtocol], float]:
        """
        Gets a dictionary with the reinforcements present at all
        locations of the cluster (`infra_cluster`) as well as their
        total cost if said reinforcement is applied at them.

        Args:
            infra_cluster (InfraCluster): Cluster being analyzed.

        Returns:
            dict[type[ReinforcementProfileProtocol], float]:
                Resulting reinforcement type - costs dictionary.
        """
        # Define initial costs
        _costs_dict = defaultdict(lambda: 0.0)
        _costs_dict[infra_cluster.reinforcement_type] = infra_cluster.current_cost

        # Get common measures excluding the initial one to reduce computations.
        _common_available_measures = set(
            OrderStrategy.get_default_order_for_reinforcements()
        )
        _common_available_measures.discard(infra_cluster.reinforcement_type)

        # Intersect per location
        for _cl in infra_cluster.cluster:
            _common_available_measures.intersection_update(_cl.available_measures)
            _discarded_measures = set()
            # Get only available measures **cheaper** than current state  and their cost.
            for _am in _common_available_measures:
                _costs_dict[_am] += _cl.get_reinforcement_costs(_am)
                if _costs_dict[_am] > _costs_dict[infra_cluster.reinforcement_type]:
                    # This can potentially save (a lot) of computations.
                    _discarded_measures.add(_am)
                    continue
            # Remove from common denominator discarded measures.
            _common_available_measures -= _discarded_measures
        _common_available_measures.add(infra_cluster.reinforcement_type)

        # Return dictionary of costs for common available measures
        return {
            _cd_m: _cd_v
            for _cd_m, _cd_v in _costs_dict.items()
            if _cd_m in _common_available_measures
        }

    def apply_strategy(
        self, strategy_input: StrategyInput
    ) -> list[StrategyLocationReinforcement]:
        _clustered_locations = []
        # 1. Run `OrderStrategy` to generate an initial cluster formation.
        for _infra_cluster in self._get_initial_clusters(strategy_input):
            self._set_cheapest_measure_per_cluster(_infra_cluster, strategy_input)
            _clustered_locations.extend(_infra_cluster.cluster)
        return _clustered_locations

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
            _infra_cluster_list.append(
                InfraCluster(reinforcement_type=_grouped_by, cluster=_grouping_data)
            )
        return _infra_cluster_list

    def _set_cheapest_measure_per_cluster(
        self, infra_cluster: InfraCluster, strategy_input: StrategyInput
    ):
        # 2. Get common available measures for each cluster
        _cam_costs = self.get_common_available_measures(infra_cluster)
        # 3. Set the **cheapest** common available measure.
        infra_cluster.set_cheapest_common_available_measure(_cam_costs)
