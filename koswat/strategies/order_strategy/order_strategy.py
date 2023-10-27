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
    _structure_buffer: float
    _min_space_between_structures: float

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

    def _set_strategy_input(self, strategy_input: StrategyInput) -> None:
        self._location_matrix = strategy_input.locations_matrix
        self._structure_buffer = strategy_input.structure_min_buffer
        self._min_space_between_structures = strategy_input.structure_min_length

    def _group_by_selected_measure(
        self, location_reinforcements: list[StrategyLocationReinforcement]
    ) -> list[tuple[type[ReinforcementProfileProtocol], StrategyLocationReinforcement]]:
        return list(
            (k, list(g))
            for k, g in groupby(
                location_reinforcements,
                lambda x: x.selected_measure,
            )
        )

    def _apply_buffer(
        self, location_reinforcements: list[StrategyLocationReinforcement]
    ) -> None:
        _grouped_by_measure = self._group_by_selected_measure(location_reinforcements)
        _len_location_reinforcements = len(location_reinforcements)
        _candidates_masks = dict(
            (_rtype, [-1] * _len_location_reinforcements)
            for _rtype in self._order_reinforcement
        )
        _visited = 0
        for _profile_type, _sub_group in _grouped_by_measure:
            # Define indices.
            _lower_limit = int(max(0, _visited - self._structure_buffer))
            _new_visited = _visited + len(_sub_group)
            _upper_limit = int(
                min(
                    _new_visited + self._structure_buffer,
                    _len_location_reinforcements - 1,
                )
            )
            _candidate_value = self._order_reinforcement.index(_profile_type)

            # Update masks
            _candidates_masks[_profile_type][_lower_limit:_new_visited] = [
                _candidate_value
            ] * (_new_visited - _lower_limit)

            _candidates_masks[_profile_type][_visited:_upper_limit] = [
                _candidate_value
            ] * (_upper_limit - _visited)

            # Update visited
            _visited = _new_visited

        # Combine dicts and get max value as "higher values" cannot use
        # a "lower value" buffer.
        _selection_mask = list(map(max, zip(*_candidates_masks.values())))

        # Apply buffer values.
        for _idx, _location in enumerate(location_reinforcements):
            _location.selected_measure = self._order_reinforcement[
                _selection_mask[_idx]
            ]

    def _apply_min_distance(
        self, location_reinforcements: list[StrategyLocationReinforcement]
    ) -> None:
        """
        Updates a location's measure type by iterating as many times as
        measures without the minimal distance are found in an initial grouping
        of locations per measures ('subtrajects').
        """
        _grouped_by_measure = self._group_by_selected_measure(location_reinforcements)

        def _get_non_compliant() -> int:
            return sum(
                len(rg) < self._min_space_between_structures
                for _, rg in _grouped_by_measure
            )

        _non_compliant_exceptions = 0
        _max_iterations = _get_non_compliant()
        for _n in range(0, _max_iterations):

            # We know we have `n` non-compliant groups,
            # it means a maximum of `n` iterations is needed
            # to correct the selected measures.
            _non_compliant_exceptions = self._apply_min_distance_to_grouped_locations(
                _grouped_by_measure
            )

            # Generate a new grouping.
            _grouped_by_measure = self._group_by_selected_measure(
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
                    _non_compliant_exceptions, self._min_space_between_structures
                )
            )

    def _apply_min_distance_to_grouped_locations(
        self,
        locations_by_measure: list[
            tuple[type[ReinforcementProfileProtocol], StrategyLocationReinforcement]
        ],
    ) -> int:
        """
        Single iteration where we go through the 'subtrajects' that do not have a measure
        meeting the minimal length requirement.
        If any of its neighbors is a higher reinforcement type then it will be adapted.
        Otherwise it will preserve its state as a 'non_compliant' exception.
        """
        _non_compliant_exceptions = 0
        for _idx, (_profile_type, _sub_group) in enumerate(locations_by_measure):
            if len(_sub_group) >= self._min_space_between_structures:
                continue
            _current_value = self._order_reinforcement.index(_profile_type)

            _previous_value = (
                -1
                if _idx - 1 < 0
                else self._order_reinforcement.index(locations_by_measure[_idx - 1][0])
            )
            _next_value = (
                -1
                if _idx + 1 >= len(locations_by_measure)
                else self._order_reinforcement.index(locations_by_measure[_idx + 1][0])
            )

            # DESIGN / THEORY decission:
            # We ensure no construction is replaced by a "lower" type.
            # This means a "short" `StabilityWallReinforcementProfile` won't be
            # replaced by a `SoilReinforcementProfile` and so on.
            _candidates = list(
                filter(lambda x: x > _current_value, [_previous_value, _next_value])
            )
            if not _candidates:
                _selected_measure_idx = _current_value
            else:
                _selected_measure_idx = max(_current_value, min(_candidates))

            _selected_measure = self._order_reinforcement[_selected_measure_idx]

            if _current_value == _selected_measure_idx:
                _non_compliant_exceptions += 1
                logging.warning(
                    "Measure {} not corrected despite length as both sides ({}, {}) are inferior reinforcement types.".format(
                        self._order_reinforcement[_current_value],
                        self._order_reinforcement[_previous_value],
                        self._order_reinforcement[_next_value],
                    )
                )
                continue

            # To avoid the next iteration wrongly setting a new measure for the next group
            # without updating the current, we need to inject the current values there.
            # This way the 'subtraject' is updated.
            if _selected_measure_idx == _next_value:
                locations_by_measure[_idx + 1] = (
                    locations_by_measure[_idx + 1][0],
                    _sub_group + locations_by_measure[_idx + 1][1],
                )

            for _loc_reinf in _sub_group:
                _loc_reinf.selected_measure = _selected_measure

        return _non_compliant_exceptions

    def _get_locations_as_strategy_reinforcements(
        self,
    ) -> list[StrategyLocationReinforcement]:
        _strategy_reinforcements = []
        for (
            _location,
            _reinforcements,
        ) in self._location_matrix.items():
            _selected_reinforcement = next(
                (_or for _or in self._order_reinforcement if _or in _reinforcements),
                self._order_reinforcement[-1],
            )
            _strategy_reinforcements.append(
                StrategyLocationReinforcement(
                    location=_location,
                    available_measures=_reinforcements,
                    selected_measure=_selected_reinforcement,
                )
            )
        return _strategy_reinforcements

    def apply_strategy(
        self, strategy_input: StrategyInput
    ) -> list[StrategyLocationReinforcement]:
        self._set_strategy_input(strategy_input)
        _strategy_reinforcements = self._get_locations_as_strategy_reinforcements()
        self._apply_buffer(_strategy_reinforcements)
        self._apply_min_distance(_strategy_reinforcements)
        return _strategy_reinforcements
