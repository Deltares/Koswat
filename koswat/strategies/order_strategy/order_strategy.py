from __future__ import annotations
from typing import Type
from itertools import groupby
from koswat.cost_report.summary.koswat_summary_location_matrix import (
    KoswatSummaryLocationMatrix,
)

from koswat.dike_reinforcements.reinforcement_profile.outside_slope.cofferdam_reinforcement_profile import (
    CofferdamReinforcementProfile,
)
from koswat.dike_reinforcements.reinforcement_profile.reinforcement_profile import (
    ReinforcementProfile,
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
from koswat.strategies.strategy_location_matrix import StrategyLocationReinforcements


class OrderStrategy:
    _location_matrix: KoswatSummaryLocationMatrix
    _order_reinforcement: list[Type[ReinforcementProfile]]
    _structure_buffer: float
    _min_space_between_structures: float

    @classmethod
    def from_strategy_input(cls, strategy_input: StrategyInput) -> OrderStrategy:
        _new_cls = cls()
        _new_cls._order_reinforcement = [
            SoilReinforcementProfile,
            PipingWallReinforcementProfile,
            StabilityWallReinforcementProfile,
            CofferdamReinforcementProfile,
        ]
        _new_cls._location_matrix = strategy_input.locations_matrix
        _new_cls._structure_buffer = strategy_input.structure_buffer
        _new_cls._min_space_between_structures = (
            strategy_input.min_space_between_structures
        )
        return _new_cls

    def _group_by_selected_measure(
        self, location_reinforcements: list[StrategyLocationReinforcements]
    ) -> list[StrategyLocationReinforcements]:
        return list(
            (k, list(g))
            for k, g in groupby(
                location_reinforcements,
                lambda x: x.selected_measure,
            )
        )

    def _apply_buffer(
        self, location_reinforcements: list[StrategyLocationReinforcements]
    ) -> None:
        _grouped_by_measure = self._group_by_selected_measure(location_reinforcements)
        _len_location_reinforcements = len(location_reinforcements)
        _candidates_matrix = dict(
            (_rtype, [-1] * _len_location_reinforcements)
            for _rtype in self._order_reinforcement
        )
        _visited = 0
        for _profile_type, _sub_group in _grouped_by_measure:
            # Define indices.
            _lower_limit = max(0, _visited - self._structure_buffer)
            _new_visited = _visited + len(_sub_group)
            _upper_limit = min(
                _new_visited + self._structure_buffer,
                _len_location_reinforcements - _new_visited,
            )
            _candidate_value = self._order_reinforcement.index(_profile_type)

            # Update matrices
            _candidates_matrix[_profile_type][_lower_limit:_new_visited] = [
                _candidate_value
            ] * (_new_visited - _lower_limit)

            _candidates_matrix[_profile_type][_visited:_upper_limit] = [
                _candidate_value
            ] * (_upper_limit - _visited)

            # Update visited
            _visited = _new_visited

        # Combine dicts and get max value as "higher values" cannot use
        # a "lower value" buffer.
        _selection_mask = list(map(max, zip(*_candidates_matrix.values())))

        # Apply buffer values.
        for _idx, _location in enumerate(location_reinforcements):
            _location.selected_measure = self._order_reinforcement[
                _selection_mask[_idx]
            ]

    def _apply_min_distance(
        self, location_reinforcements: list[StrategyLocationReinforcements]
    ) -> None:
        _grouped_by_measure = self._group_by_selected_measure(location_reinforcements)
        # TODO: Discuss recursivity if we leave the current value (line 111 and 122).
        # if all(len(rg) >= self._min_space_between_structures for _, rg in _grouped):
        #     return
        for _idx, (_profile_type, _sub_group) in enumerate(_grouped_by_measure):
            if len(_sub_group) >= self._min_space_between_structures:
                continue
            _current_value = self._order_reinforcement.index(_profile_type)
            _previous_value = (
                -1
                if _idx - 1 < 0
                else self._order_reinforcement.index(_grouped_by_measure[_idx - 1][0])
            )
            _next_value = (
                -1
                if _idx + 1 >= len(_grouped_by_measure)
                else self._order_reinforcement.index(_grouped_by_measure[_idx + 1][0])
            )
            _selected_measure = self._order_reinforcement[
                max(_current_value, min(_previous_value, _next_value))
            ]
            for _loc_reinf in _sub_group:
                _loc_reinf.selected_measure = _selected_measure

    def get_locations_reinforcements(
        self,
    ) -> list[StrategyLocationReinforcements]:
        _strategy_reinforcements = []
        for (
            _location,
            _reinforcements,
        ) in self._location_matrix.locations_matrix.items():
            _selected_reinforcement = next(
                (_or for _or in self._order_reinforcement if _or in _reinforcements),
                self._order_reinforcement[-1],
            )
            _strategy_reinforcements.append(
                StrategyLocationReinforcements(
                    location=_location,
                    available_measures=_reinforcements,
                    selected_measure=_selected_reinforcement,
                )
            )
        self._apply_buffer(_strategy_reinforcements)
        self._apply_min_distance(_strategy_reinforcements)
        return _strategy_reinforcements
