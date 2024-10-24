from collections import defaultdict
from itertools import groupby

from koswat.dike_reinforcements.reinforcement_profile.reinforcement_profile_protocol import (
    ReinforcementProfileProtocol,
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

    def _get_initial_clusters(
        self, strategy_input: StrategyInput
    ) -> list[StrategyLocationReinforcement]:
        return OrderStrategy().apply_strategy(strategy_input)

    def _get_common_available_measures(
        self,
        initial_measure: type[ReinforcementProfileProtocol],
        clustered_locations: list[StrategyLocationReinforcement],
    ) -> dict[type[ReinforcementProfileProtocol], float]:
        # Define initial costs
        _costs_dict = defaultdict(lambda: 0.0)
        _costs_dict[initial_measure] = sum(
            _c.current_cost for _c in clustered_locations
        )

        # Get common measures excluding the initial one to reduce computations.
        _common_available_measures = set(
            OrderStrategy.get_default_order_for_reinforcements()
        )
        _common_available_measures.discard(initial_measure)

        # Intersect per location
        for _cl in clustered_locations:
            _common_available_measures.intersection_update(_cl.available_measures)
            _discarded_measures = set()
            # Get only available measures **cheaper** than current state  and their cost.
            for _am in _common_available_measures:
                _costs_dict[_am] += clustered_locations[0].get_reinforcement_costs(_am)
                if _costs_dict[_am] > _costs_dict[initial_measure]:
                    # This can potentially save (a lot) of computations.
                    _discarded_measures.add(_am)
                    continue
            # Remove from common denominator discarded measures.
            _common_available_measures -= _discarded_measures
        _common_available_measures.add(initial_measure)

        # Return dictionary of costs for common available measures
        return {
            _cd_m: _cd_v
            for _cd_m, _cd_v in _costs_dict.items()
            if _cd_m in _common_available_measures
        }

    def _set_cheapest_common_available_measure(
        self,
        initial_measure: type[ReinforcementProfileProtocol],
        cluster_data: list[StrategyLocationReinforcement],
        measure_costs: dict[type[ReinforcementProfileProtocol]],
    ):
        # 3.1. Get the cheapest common available measure.
        _selection = min(
            measure_costs,
            key=measure_costs.get,
        )

        # 3.2. Set the selection if different from the initial.
        if _selection != initial_measure:
            for _cd in cluster_data:
                _cd.selected_measure = _selection

    def apply_strategy(
        self, strategy_input: StrategyInput
    ) -> list[StrategyLocationReinforcement]:
        # 1. Run `OrderStrategy` to generate an initial cluster formation.
        _clustered_locations = self._get_initial_clusters(strategy_input)

        # Now, for each cluster
        for _initial_measure, _cluster in groupby(
            _clustered_locations, key=lambda x: x.selected_measure
        ):
            _cluster_data = list(_cluster)
            if not any(_cluster_data):
                continue

            # 2. Get common available measures for each cluster
            _cam_costs = self._get_common_available_measures(
                _initial_measure, _cluster_data
            )

            # 3. Set the **cheapest** common available measure.
            self._set_cheapest_common_available_measure(
                _initial_measure, _cluster_data, _cam_costs
            )
        return _clustered_locations
