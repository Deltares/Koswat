from __future__ import annotations
import logging
from typing import Type
from itertools import groupby
from koswat.dike.surroundings.point.point_surroundings import PointSurroundings

from koswat.dike_reinforcements.reinforcement_profile.outside_slope.cofferdam_reinforcement_profile import (
    CofferdamReinforcementProfile,
)
from koswat.dike_reinforcements.reinforcement_profile.reinforcement_profile_protocol import (
    ReinforcementProfileProtocol,
)
from koswat.dike_reinforcements.reinforcement_profile.standard.piping_wall_reinforcement_profile import (
    PipingWallReinforcementProfile,
)
from koswat.dike_reinforcements.reinforcement_profile.standard.soil_reinforcement_profile import (
    SoilReinforcementProfile,
)
from koswat.dike_reinforcements.reinforcement_profile.standard.stability_wall_reinforcement_profile import (
    StabilityWallReinforcementProfile,
)
from koswat.strategies.order_strategy.order_cluster import (
    OrderCluster,
)
from koswat.strategies.strategy_input import StrategyInput
from koswat.strategies.strategy_location_reinforcement import (
    StrategyLocationReinforcement,
)
from koswat.strategies.strategy_protocol import StrategyProtocol


class OrderStrategy(StrategyProtocol):
    _location_matrix: dict[PointSurroundings, list[Type[ReinforcementProfileProtocol]]]
    _order_reinforcement: list[Type[ReinforcementProfileProtocol]]
    _structure_min_buffer: float
    _structure_min_length: float

    def __init__(self) -> None:
        self._order_reinforcement = self.get_default_order_for_reinforcements()

    @staticmethod
    def get_default_order_for_reinforcements() -> list[
        Type[ReinforcementProfileProtocol]
    ]:
        return [
            SoilReinforcementProfile,
            PipingWallReinforcementProfile,
            StabilityWallReinforcementProfile,
            CofferdamReinforcementProfile,
        ]

    @staticmethod
    def get_strategy_reinforcements(
        location_matrix: dict[
            PointSurroundings, list[Type[ReinforcementProfileProtocol]]
        ],
        selection_order: list[Type[ReinforcementProfileProtocol]],
    ) -> list[StrategyLocationReinforcement]:
        _strategy_reinforcements = []
        for (
            _location,
            _reinforcements,
        ) in location_matrix.items():
            _selected_reinforcement = next(
                (_or for _or in selection_order if _or in _reinforcements),
                selection_order[-1],
            )
            _strategy_reinforcements.append(
                StrategyLocationReinforcement(
                    location=_location,
                    available_measures=_reinforcements,
                    selected_measure=_selected_reinforcement,
                )
            )
        return _strategy_reinforcements

    def _set_strategy_input(self, strategy_input: StrategyInput) -> None:
        self._location_matrix = strategy_input.locations_matrix
        self._structure_min_buffer = strategy_input.structure_min_buffer
        self._structure_min_length = strategy_input.structure_min_length

    def _get_reinforcement_clusters(
        self, location_reinforcements: list[StrategyLocationReinforcement]
    ) -> list[int, StrategyLocationReinforcement]:
        return list(
            (self._order_reinforcement.index(k), list(g))
            for k, g in groupby(
                location_reinforcements,
                lambda x: x.selected_measure,
            )
        )

    def _get_reinforcement_order_clusters(
        self, location_reinforcements: list[StrategyLocationReinforcement]
    ) -> list[OrderCluster]:
        _added_clusters = []
        for _cluster in self._get_reinforcement_clusters(location_reinforcements):
            _last_added = OrderCluster(
                reinforcement_idx=_cluster[0],
                location_reinforcements=_cluster[1],
                left_neighbor=_added_clusters[-1] if any(_added_clusters) else None,
            )
            if isinstance(_last_added.left_neighbor, OrderCluster):
                _last_added.left_neighbor.right_neighbor = _last_added
            _added_clusters.append(_last_added)
        return _added_clusters

    def _get_buffer_mask(
        self, location_reinforcements: list[StrategyLocationReinforcement]
    ) -> list[int]:
        _idx_clustering = self._get_reinforcement_clusters(location_reinforcements)
        _len_location_reinforcements = len(location_reinforcements)
        _candidates_masks = dict(
            (_r_idx, [-1] * _len_location_reinforcements)
            for _r_idx in range(0, len(self._order_reinforcement))
        )
        _visited = 0
        for _reinforcement_idx, _sub_group in _idx_clustering:
            # Define indices.
            _lower_limit = int(max(0, _visited - self._structure_min_buffer))
            _new_visited = _visited + len(_sub_group)
            _upper_limit = int(
                min(
                    _new_visited + self._structure_min_buffer,
                    _len_location_reinforcements - 1,
                )
            )

            # Update masks
            _candidates_masks[_reinforcement_idx][_lower_limit:_new_visited] = [
                _reinforcement_idx
            ] * (_new_visited - _lower_limit)

            _candidates_masks[_reinforcement_idx][_visited:_upper_limit] = [
                _reinforcement_idx
            ] * (_upper_limit - _visited)

            # Update visited
            _visited = _new_visited

        # Combine dicts and get max value as "higher values" cannot use
        # a "lower value" buffer.
        return list(map(max, zip(*_candidates_masks.values())))

    def _apply_buffering(
        self, location_reinforcements: list[StrategyLocationReinforcement]
    ) -> None:
        _result_mask = self._get_buffer_mask(location_reinforcements)

        # Apply buffer values.
        for _idx, _location in enumerate(location_reinforcements):
            _location.selected_measure = self._order_reinforcement[_result_mask[_idx]]

    def _apply_clustering(
        self, location_reinforcements: list[StrategyLocationReinforcement]
    ) -> None:
        """
        Updates a location's measure type by iterating as many times as
        measures without the minimal distance are found in an initial grouping
        of locations per measures ('subtrajects').
        """
        _available_clusters = self._get_reinforcement_order_clusters(
            location_reinforcements
        )
        _reinforcements_order_max_idx = len(self._order_reinforcement)
        for _target_reinforcement_idx in range(0, _reinforcements_order_max_idx):
            _target_non_compliant_clusters = list(
                filter(
                    lambda x: not x.is_compliant(
                        self._structure_min_length, self._order_reinforcement[-1]
                    )
                    and x.reinforcement_idx == _target_reinforcement_idx,
                    _available_clusters,
                )
            )
            if not any(_target_non_compliant_clusters):
                break

            for _cluster in _target_non_compliant_clusters:
                if _cluster.is_compliant(
                    self._structure_min_length, _reinforcements_order_max_idx
                ):
                    continue

                _stronger_cluster = _cluster.get_stronger_cluster()
                if _stronger_cluster == _cluster:
                    logging.warning(
                        "Cluster for {} not merged despite length at traject order {} - {}, as both sides ({}, {}) are inferior reinforcement types.".format(
                            self._order_reinforcement[_cluster.reinforcement_idx],
                            _cluster.location_reinforcements[0].location.traject_order,
                            _cluster.location_reinforcements[-1].location.traject_order,
                            self._order_reinforcement[
                                _cluster.left_neighbor.reinforcement_idx
                            ],
                            self._order_reinforcement[
                                _cluster.right_neighbor.reinforcement_idx
                            ],
                        )
                    )
                    continue

                # Update selected measures for locations in this cluster.
                _stronger_cluster.merge_cluster(_cluster)
                _available_clusters.pop(_available_clusters.index(_cluster))

    def apply_strategy(
        self, strategy_input: StrategyInput
    ) -> list[StrategyLocationReinforcement]:
        self._set_strategy_input(strategy_input)
        _strategy_reinforcements = self.get_strategy_reinforcements(
            self._location_matrix, self.get_default_order_for_reinforcements()
        )
        self._apply_buffering(_strategy_reinforcements)
        self._apply_clustering(_strategy_reinforcements)
        return _strategy_reinforcements
