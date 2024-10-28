from dataclasses import dataclass, field
from typing import Type

from koswat.dike.surroundings.point.point_surroundings import PointSurroundings
from koswat.dike_reinforcements.reinforcement_profile.reinforcement_profile_protocol import (
    ReinforcementProfileProtocol,
)
from koswat.strategies.strategy_reinforcement_type_costs import (
    StrategyReinforcementTypeCosts,
)


@dataclass
class StrategyLocationInput:
    point_surrounding: PointSurroundings
    strategy_reinforcement_type_costs: list[StrategyReinforcementTypeCosts] = field(
        default_factory=lambda: []
    )

    @property
    def cheapest_reinforcement(self) -> StrategyReinforcementTypeCosts:
        """
        Gets the `StrategyLocationReinforcementCosts` with the lower `total_costs` value.
        Returns:
            StrategyLocationReinforcementCosts: The cheapest reinforcement for this location.
        """
        return min(self.strategy_reinforcement_type_costs, key=lambda x: x.total_costs)

    @property
    def available_measures(self) -> list[Type[ReinforcementProfileProtocol]]:
        """
        Gets all the available reinforcement types in `strategy_location_reinforcements`.
        It is called `available_measures` to match the `StrategyLocationReinforcement`
        definition.

        Returns:
            list[Type[ReinforcementProfileProtocol]]: resulting list.
        """
        return [
            _slr.reinforcement_type for _slr in self.strategy_reinforcement_type_costs
        ]

    def get_reinforcement_costs(
        self, reinforcement_type: type[ReinforcementProfileProtocol]
    ) -> float:
        for _srtc in self.strategy_reinforcement_type_costs:
            if _srtc.reinforcement_type == reinforcement_type:
                return _srtc.total_costs
        raise ValueError(
            f"Reinforcement {reinforcement_type.output_name} not available, costs cannot be computed."
        )

    def get_infrastructure_costs(
        self, reinforcement_type: type[ReinforcementProfileProtocol]
    ) -> tuple[float, float]:
        for _srtc in self.strategy_reinforcement_type_costs:
            if _srtc.reinforcement_type == reinforcement_type:
                return (
                    _srtc.infrastructure_costs,
                    _srtc.infrastructure_costs_with_surtax,
                )
        raise ValueError(
            f"Reinforcement {reinforcement_type.output_name} not available, costs cannot be computed."
        )
