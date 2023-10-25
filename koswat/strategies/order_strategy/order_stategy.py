from collections import defaultdict
from typing import Type
from koswat.cost_report.summary.koswat_summary_location_matrix import (
    KoswatSummaryLocationMatrix,
)

from koswat.dike.surroundings.point.point_surroundings import PointSurroundings
from koswat.dike_reinforcements.reinforcement_profile.outside_slope import (
    cofferdam_reinforcement_profile,
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


class OrderStrategy:
    _location_matrix: KoswatSummaryLocationMatrix
    _order_reinforcement: list[Type[ReinforcementProfile]]
    _structure_buffer: float
    _min_space_between_structures: float

    def __init__(self, strategy_input: StrategyInput) -> None:
        self._order_reinforcement = [
            SoilReinforcementProfile,
            PipingWallReinforcementProfile,
            StabilityWallReinforcementProfile,
            cofferdam_reinforcement_profile,
        ]
        self._location_matrix = strategy_input.locations_matrix
        self._structure_buffer = strategy_input.structure_buffer
        self._min_space_between_structures = strategy_input.min_space_between_structures

    def get_locations_reinforcements(
        self,
    ) -> dict[PointSurroundings, ReinforcementProfile]:
        # Ensure it's ordered
        self._location_matrix.get_order_by_location()

        _first_choice = defaultdict(list)
        for (
            _location,
            _reinforcements,
        ) in self._location_matrix.locations_matrix.items():
            _first_choice[_location] = next(
                (_or for _or in self._order_reinforcement if _or in _reinforcements),
                self._order_reinforcement[-1],
            )

        return dict(_first_choice)
