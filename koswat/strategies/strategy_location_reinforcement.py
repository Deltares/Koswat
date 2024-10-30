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

    _selected_measures: list[type[ReinforcementProfileProtocol]] = field(
        default_factory=lambda: [None, None, None]
    )

    def __post_init__(self):
        if any(self.available_measures):
            # Set the inital selection to the first available measure.
            self.current_selected_measure = self.available_measures[0]

    @property
    def current_selected_measure(self) -> type[ReinforcementProfileProtocol]:
        """
        Exposes the current selected measure for this object.
        """
        return self._selected_measures[-1]

    @current_selected_measure.setter
    def current_selected_measure(
        self, reinforcement_type: type[ReinforcementProfileProtocol]
    ):
        # We only want to keep [Initial, Step, Current] selection history
        if not self._selected_measures[0]:
            self._selected_measures = [reinforcement_type] * 3
            return

        # Shift the current to "step" and add the new one
        self._selected_measures[1:] = [self._selected_measures[2], reinforcement_type]

    @property
    def previous_selected_measure(self) -> type[ReinforcementProfileProtocol]:
        """
        Exposes the selected measure previous to the current one.
        Expected at least three steps:
            - 0, first selection, without clustering.
            - 1, selection based on traject's buffer + clustering.
            - 2, selection based on optimal  infrastructure's costs.
        """
        if not self._selected_measures:
            return None
        if len(self._selected_measures) > 2:
            return self._selected_measures[-2]
        # If no "in-between" step was found, then just pick the last one.
        return self._selected_measures[-1]

    @property
    def current_cost(self) -> float:
        """
        Estimates the costs at this location for the given `selected_measure`.
        """
        if not self.current_selected_measure or not self.strategy_location_input:
            return 0.0
        for _srtc in self.strategy_location_input.strategy_reinforcement_type_costs:
            if _srtc.reinforcement_type == self.current_selected_measure:
                return _srtc.total_costs
        return 0.0
        # raise ValueError("No current cost could be calculated")

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
