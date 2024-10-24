from dataclasses import dataclass, field
from typing import Type

from koswat.dike.surroundings.point.point_surroundings import PointSurroundings
from koswat.dike_reinforcements.reinforcement_profile.reinforcement_profile_protocol import (
    ReinforcementProfileProtocol,
)


@dataclass
class StrategyLocationReinforcementCosts:
    reinforcement_type: Type[ReinforcementProfileProtocol]
    base_costs: float = 0.0
    infastructure_costs: float = 0.0

    @property
    def total_costs(self) -> float:
        """
        The simple addition of the base costs and the possible
        related infrastructure costs.
        Returns:
            float: The total costs when applying this reinforcement.
        """
        return self.base_costs + self.infastructure_costs


@dataclass
class StrategyLocation:
    point_surrounding: PointSurroundings
    available_reinforcements: list[StrategyLocationReinforcementCosts] = field(
        default_factory=lambda: []
    )

    @property
    def cheapest_reinforcment(self) -> StrategyLocationReinforcementCosts:
        """
        Gets the `StrategyLocationReinforcementCosts` with the lower `total_costs` value.
        Returns:
            StrategyLocationReinforcementCosts: The cheapest reinforcement for this location.
        """
        return min(self.available_reinforcements, key=lambda x: x.total_costs)

    @property
    def reinforcement_types(self) -> list[Type[ReinforcementProfileProtocol]]:
        """
        Gets all the available reinforcement types in `strategy_location_reinforcements`.

        Returns:
            list[Type[ReinforcementProfileProtocol]]: resulting list.
        """
        return [_slr.reinforcement_type for _slr in self.available_reinforcements]


@dataclass
class StrategyInput:
    strategy_locations: list[StrategyLocation]
    reinforcement_min_buffer: float
    reinforcement_min_length: float
