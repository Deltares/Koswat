"""
                    GNU GENERAL PUBLIC LICENSE
                      Version 3, 29 June 2007

    KOSWAT, from the dutch combination of words `Kosts-Wat` (what are the costs)
    Copyright (C) 2024 Stichting Deltares

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program.  If not, see <http://www.gnu.org/licenses/>.
"""

from dataclasses import dataclass, field

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
        Gets the `StrategyLocationReinforcementCosts` with the lowest `total_costs_with_surtax` value.

        Returns:
            StrategyLocationReinforcementCosts: The cheapest reinforcement for this location.
        """
        return min(
            self.strategy_reinforcement_type_costs,
            key=lambda x: x.total_costs_with_surtax,
        )

    @property
    def available_measures(self) -> list[type[ReinforcementProfileProtocol]]:
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
        """
        Get the costs for the given reinforcement type.

        Args:
            reinforcement_type (type[ReinforcementProfileProtocol]): The reinforcement type.

        Raises:
            ValueError: The reinforcement type is not available.

        Returns:
            float: The reinforcement costs with surtax.
        """
        for _srtc in self.strategy_reinforcement_type_costs:
            if _srtc.reinforcement_type == reinforcement_type:
                return _srtc.total_costs_with_surtax
        raise ValueError(
            f"Reinforcement {reinforcement_type.output_name} not available, costs cannot be computed."
        )

    def get_infrastructure_costs(
        self, reinforcement_type: type[ReinforcementProfileProtocol]
    ) -> tuple[float, float]:
        """
        Get the infrastructure costs for the given reinforcement type.

        Args:
            reinforcement_type (type[ReinforcementProfileProtocol]): The reinforcement type.

        Raises:
            ValueError: The reinforcement type is not available.

        Returns:
            tuple[float, float]: Tuple containing the infrastructure costs without and with surtax.
        """
        for _srtc in self.strategy_reinforcement_type_costs:
            if _srtc.reinforcement_type == reinforcement_type:
                return (
                    _srtc.infrastructure_costs,
                    _srtc.infrastructure_costs_with_surtax,
                )
        raise ValueError(
            f"Reinforcement {reinforcement_type.output_name} not available, costs cannot be computed."
        )
