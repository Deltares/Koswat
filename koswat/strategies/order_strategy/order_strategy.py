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

    def _apply_buffer(
        self, location_reinforcements: list[StrategyLocationReinforcement]
    ) -> None:
        _result_mask = self._get_buffer_mask(location_reinforcements)

        # Apply buffer values.
        for _idx, _location in enumerate(location_reinforcements):
            _location.selected_measure = self._order_reinforcement[_result_mask[_idx]]

    def _apply_min_distance(
        self, location_reinforcements: list[StrategyLocationReinforcement]
    ) -> None:
        """
        Updates a location's measure type by iterating as many times as
        measures without the minimal distance are found in an initial grouping
        of locations per measures ('subtrajects').
        """
        _reinforcement_idx_clusters = self._get_reinforcement_clusters(
            location_reinforcements
        )

        def _get_non_compliant() -> int:
            return sum(
                len(rg) < self._structure_min_length
                for r_idx, rg in _reinforcement_idx_clusters
                if r_idx != len(self._order_reinforcement) -1
            )

        _non_compliant_exceptions = 0
        _max_iterations = _get_non_compliant()

        # We know we have `n` non-compliant groups,
        # it means a maximum of `n` iterations is needed
        # to correct the selected measures.

        for _n in range(0, _max_iterations):

            _non_compliant_exceptions = self._apply_min_distance_to_clusters(
                _reinforcement_idx_clusters
            )

            # Generate a new grouping.
            _reinforcement_idx_clusters = self._get_reinforcement_clusters(
                location_reinforcements
            )

            _non_compliant_groups = _get_non_compliant()

            if (
                _non_compliant_groups == 0
                or _non_compliant_groups == _non_compliant_exceptions
            ):
                # No need to look further.
                logging.debug(
                    "Measures corrected after {} iterations of the `_apply_min_distance` algorithm.".format(
                        _n
                    )
                )
                break

        if _non_compliant_exceptions > 0:
            logging.warning(
                "There are {} which could not fulfill the minimal distance of {} meters.".format(
                    _non_compliant_exceptions, self._structure_min_length
                )
            )

    def _apply_min_distance_to_clusters(
        self,
        reinforcement_idx_clusters: list[int, list[StrategyLocationReinforcement]],
    ) -> int:
        """
        We iterate through the 'subtrajects' that do not have a measure meeting the
        minimal length requirement.
        We need to increment the 'strength' of non-compliant clusters in the strategy's
        default order. The last type can be skipped as it cannot be futher strengthen.
        If any of its neighbors is a higher reinforcement type then it will be adapted.
        Otherwise it will preserve its state as a 'non-compliant' exception.
        """
        _non_compliant_exceptions = 0
        for _target_reinforcement_idx in range(0, len(self._order_reinforcement) - 1):
            for _idx, (_reinforcement_idx, _cluster) in enumerate(
                reinforcement_idx_clusters
            ):
                if (
                    _reinforcement_idx != _target_reinforcement_idx
                    or len(_cluster) >= self._structure_min_length
                    or not any(_cluster)
                ):
                    continue

                _previous_value = (
                    -1 if _idx - 1 < 0 else reinforcement_idx_clusters[_idx - 1][0]
                )
                _next_value = (
                    -1
                    if _idx + 1 >= len(reinforcement_idx_clusters)
                    else reinforcement_idx_clusters[_idx + 1][0]
                )

                # DESIGN / THEORY decission:
                # We ensure no construction is replaced by a "lower" type.
                # This means a "short" `StabilityWallReinforcementProfile` won't be
                # replaced by a `SoilReinforcementProfile` and so on.
                _selected_measure_idx = min(
                    filter(
                        lambda x: x > _reinforcement_idx, [_previous_value, _next_value]
                    ),
                    default=_reinforcement_idx,
                )

                if _reinforcement_idx == _selected_measure_idx:
                    _non_compliant_exceptions += 1
                    logging.warning(
                        "Measure {} not corrected despite length as both sides ({}, {}) are inferior reinforcement types.".format(
                            self._order_reinforcement[_reinforcement_idx],
                            self._order_reinforcement[_previous_value],
                            self._order_reinforcement[_next_value],
                        )
                    )
                    continue

                # Update selected measures for locations in this cluster.
                for _loc_reinf in _cluster:
                    _loc_reinf.selected_measure = self._order_reinforcement[
                        _selected_measure_idx
                    ]

                # Update clusters.
                # We merge first towards the "next" cluster, in case both sides have the
                # same type of reinforcement, to prevent it from being too short in the
                # upcoming iteration, therefore going again through all this code..

                reinforcement_idx_clusters[_idx] = (_selected_measure_idx, [])
                if _selected_measure_idx == _next_value:
                    reinforcement_idx_clusters[_idx + 1] = (
                        reinforcement_idx_clusters[_idx + 1][0],
                        _cluster + reinforcement_idx_clusters[_idx + 1][1],
                    )
                else:
                    reinforcement_idx_clusters[_idx - 1] = (
                        reinforcement_idx_clusters[_idx - 1][0],
                        reinforcement_idx_clusters[_idx - 1][1] + _cluster,
                    )

        return _non_compliant_exceptions

    def apply_strategy(
        self, strategy_input: StrategyInput
    ) -> list[StrategyLocationReinforcement]:
        self._set_strategy_input(strategy_input)
        _strategy_reinforcements = self.get_strategy_reinforcements(
            self._location_matrix, self.get_default_order_for_reinforcements()
        )
        self._apply_buffer(_strategy_reinforcements)
        self._apply_min_distance(_strategy_reinforcements)
        return _strategy_reinforcements
