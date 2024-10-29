from dataclasses import dataclass, field

from koswat.dike.surroundings.point.point_surroundings import PointSurroundings
from koswat.dike_reinforcements.reinforcement_profile.reinforcement_profile_protocol import (
    ReinforcementProfileProtocol,
)
from koswat.strategies.strategy_input import StrategyLocationInput
from koswat.strategies.strategy_reinforcement_type_costs import (
    StrategyReinforcementTypeCosts,
)


@dataclass
class StrategyLocationReinforcement:
    """
    Represents a location and the different reinforcements that can be applied to it
    as well their costs.
    This class is used to show the final chosen state for a location.
    """

    location: PointSurroundings
    available_measures: list[type[ReinforcementProfileProtocol]]
    strategy_location_input: StrategyLocationInput = None

    _selected_measures: list = field(default_factory=lambda: [])

    @property
    def selected_measure(self) -> type[ReinforcementProfileProtocol]:
        """
        Exposes the current selected measure for this object.
        """
        if not self._selected_measures:
            return None
        return self._selected_measures[-1]

    @selected_measure.setter
    def selected_measure(self, reinforcement_type: type[ReinforcementProfileProtocol]):
        self._selected_measures.append(reinforcement_type)

    @property
    def selection_measure_steps(self) -> list[type[ReinforcementProfileProtocol]]:
        """
        READ-ONLY property. Exposes the different selected measures for this reinforcement.
        We consider the last item the current selection, so from older to newer.
        """
        return self._selected_measures

    @property
    def current_cost(self) -> float:
        """
        Estimates the costs at this location for the given `selected_measure`.
        """
        if not self.selected_measure or not self.strategy_location_input:
            return 0.0
        for _srtc in self.strategy_location_input.strategy_reinforcement_type_costs:
            if _srtc.reinforcement_type == self.selected_measure:
                return _srtc.total_costs
        raise ValueError("No current cost could be calculated")

    @property
    def cheapest_reinforcement(self) -> StrategyReinforcementTypeCosts:
        if not self.strategy_location_input:
            return None
        return self.strategy_location_input.cheapest_reinforcement

    def get_reinforcement_costs(
        self, reinforcement_type: type[ReinforcementProfileProtocol]
    ) -> float:
        if reinforcement_type not in self.available_measures:
            raise ValueError(
                f"Reinforcement {reinforcement_type.output_name} not available, costs cannot be computed.",
            )
        return self.strategy_location_input.get_reinforcement_costs(reinforcement_type)

    def get_infrastructure_costs(
        self, reinforcement_type: type[ReinforcementProfileProtocol]
    ) -> tuple[float, float]:
        """
        Returns the infrastructure costs for the given reinforcement type (without and with surtax).

        Args:
            reinforcement_type (type[ReinforcementProfileProtocol]): Reinforcement type.

        Returns:
            tuple[float, float]: Tuple containing the infrastructure costs without and with surtax.
        """
        if (
            self.strategy_location_input
            and reinforcement_type in self.available_measures
        ):
            return self.strategy_location_input.get_infrastructure_costs(
                reinforcement_type
            )
        return (0.0, 0.0)
