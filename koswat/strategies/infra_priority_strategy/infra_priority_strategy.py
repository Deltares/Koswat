from collections import defaultdict
from itertools import groupby

from koswat.strategies.order_strategy.order_strategy import OrderStrategy
from koswat.strategies.strategy_input import StrategyInput
from koswat.strategies.strategy_location_reinforcement import (
    StrategyLocationReinforcement,
)
from koswat.strategies.strategy_protocol import StrategyProtocol


class InfraPriorityStrategy(StrategyProtocol):
    def apply_strategy(
        self, strategy_input: StrategyInput
    ) -> list[StrategyLocationReinforcement]:
        # 1. Run `OrderStrategy` to generate an initial cluster formation.
        _initial_clusters = OrderStrategy().apply_strategy(strategy_input)

        # This strategy works under the assumption that \
        # `StrategyLocationReinforcement.available_measures`
        # ARE NOT ordered by "compatibility".
        # Thus we need to check first which are the compatible reinforcements
        # per cluster.

        _result_clusters = []

        for _initial_measure, _cluster in groupby(
            _initial_clusters, key=lambda x: x.selected_measure
        ):
            _cluster_data = list(_cluster)
            if not any(_cluster_data):
                continue

            # 2. Get common available measures for each cluster
            _common_available_measures = set(_cluster_data[0].available_measures)
            _common_available_measures.discard(_common_available_measures)
            # _initial_costs = sum(_c.current_cost for _c in _cluster_data)

            _selection = _initial_measure
            _costs_dict = defaultdict(lambda: 0.0)
            _costs_dict[_initial_measure] = sum(_c.current_cost for _c in _cluster_data)

            # Define common available measures
            for _cd in _cluster_data:
                _common_available_measures.intersection_update(_cd.available_measures)
                _discarded_measures = set()
                # Get only available measures **cheaper** than current state
                # and their cost summation.
                for _am in _common_available_measures:
                    _costs_dict[_am] += _cluster_data[0].get_reinforcement_costs(_am)
                    if _costs_dict[_am] > _costs_dict[_initial_measure]:
                        # This can potentially save (a lot) of computations.
                        _discarded_measures.add(_am)
                        continue
                _common_available_measures -= _discarded_measures

            # 3. Set the **cheapest** common available measure.
            # 3.1. Get the cheapest common available measure.
            _common_available_measures.add(_initial_measure)
            _selection = min(
                _common_available_measures,
                key=lambda x: _costs_dict[x],
            )

            # 3.2. Set the selection if different from the initial.
            if _selection != _initial_measure:
                for _cd in _cluster_data:
                    _cd.selected_measure = _selection
                _result_clusters.extend(_cluster_data)

        return _initial_clusters
