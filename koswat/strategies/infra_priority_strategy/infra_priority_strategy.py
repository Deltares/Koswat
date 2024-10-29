from __future__ import annotations

from collections import defaultdict
from itertools import groupby
from typing import Iterator

from more_itertools import windowed_complete

from koswat.dike_reinforcements.reinforcement_profile.reinforcement_profile_protocol import (
    ReinforcementProfileProtocol,
)
from koswat.strategies.infra_priority_strategy.infra_cluster import InfraCluster
from koswat.strategies.infra_priority_strategy.infra_cluster_option import (
    InfraClusterOption,
)
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
    def get_common_available_measures_costs(
        infra_cluster: InfraCluster,
    ) -> dict[type[ReinforcementProfileProtocol], float]:
        """
        Gets a dictionary with the reinforcements available at all
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

    @staticmethod
    def generate_subcluster_options(
        from_cluster: InfraCluster, min_length: int
    ) -> list[list[InfraCluster]]:
        """
        Generates all possible combinations of (sub) clusters based on the locations
        of this cluster. These are also referred as "options".

        Args:
            min_length (int): Minimum length for a cluster to be valid.

        Returns:
            list[list[InfraCluster]]: Collection of "options" with valid length.
        """

        if not from_cluster.fits_subclusters():
            # If the cluster is not twice as big as the minimum
            # required length we know there is no possibility of
            # creating subclusters.
            return [[from_cluster]]

        def get_cluster_option(
            location_collection: list[StrategyLocationReinforcement],
        ) -> list[list[InfraCluster]]:
            _icc = []
            for _w_element in filter(len, location_collection):
                _ic = InfraCluster(
                    min_required_length=from_cluster.min_required_length,
                    reinforcement_type=from_cluster.reinforcement_type,
                    cluster=list(_w_element),
                )

                if not _ic.is_valid():
                    # There is no need to check further,
                    # this option will result as not valid.
                    _icc.clear()
                    break
                _icc.append(_ic)
            return _icc

        return filter(
            any,
            map(
                get_cluster_option,
                windowed_complete(from_cluster.cluster, min_length),
            ),
        )

    def apply_strategy(
        self, strategy_input: StrategyInput
    ) -> list[StrategyLocationReinforcement]:
        _clustered_locations = []
        # 1. Run `OrderStrategy` to generate an initial cluster formation.
        for _infra_cluster in self._get_initial_state(strategy_input):
            self._set_cheapest_measure_per_cluster(_infra_cluster, strategy_input)
            _clustered_locations.extend(_infra_cluster.cluster)
        return _clustered_locations

    def _get_initial_state(
        self, strategy_input: StrategyInput
    ) -> Iterator[InfraCluster]:
        for _grouped_by, _grouping in groupby(
            OrderStrategy().apply_strategy(strategy_input),
            key=lambda x: x.selected_measure,
        ):
            _grouping_data = list(_grouping)
            if not _grouping_data:
                continue
            yield InfraCluster(
                reinforcement_type=_grouped_by,
                cluster=_grouping_data,
                min_required_length=strategy_input.reinforcement_min_cluster,
            )

    def _set_cheapest_measure_per_cluster(
        self, infra_cluster: InfraCluster, strategy_input: StrategyInput
    ):
        # 2. Get common available measures for each cluster
        _min_costs = infra_cluster.current_cost
        _selected_cluster_collection_costs = None
        for _clustering_option in self.generate_subcluster_options(
            infra_cluster, strategy_input.reinforcement_min_cluster
        ):
            _icc = InfraClusterOption(
                cluster_min_length=strategy_input.reinforcement_min_cluster,
            )
            _icc_costs = 0
            for _sub_cluster in _clustering_option:
                _icc.add_cluster(
                    _sub_cluster, self.get_common_available_measures_costs(_sub_cluster)
                )
                _icc_costs += min(_icc.cluster_costs[-1].values())
                if _icc_costs > _min_costs:
                    # No need to check further, it is more expensive already.
                    break
            if _icc_costs < _min_costs:
                # Replace cluster collection with minimal costs.
                _min_costs = _icc_costs
                _selected_cluster_collection_costs = _icc

        # 3. Set the **cheapest** common available measure.
        if _selected_cluster_collection_costs:
            # Do nothing, we did not improve the cluster.
            _selected_cluster_collection_costs.set_cheapest_option()
