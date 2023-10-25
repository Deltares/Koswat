from __future__ import annotations
from typing import Type
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
        _new_cls._min_space_between_structures = strategy_input.min_space_between_structures
        return _new_cls

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

        return _strategy_reinforcements
