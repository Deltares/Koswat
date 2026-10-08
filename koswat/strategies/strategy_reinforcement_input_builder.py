"""
                GNU GENERAL PUBLIC LICENSE
                  Version 3, 29 June 2007

KOSWAT, from the dutch combination of words `Kosts-Wat` (what are the costs)
Copyright (C) 2025 Stichting Deltares

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

from dataclasses import dataclass
from koswat.dike_reinforcements.reinforcement_profile.standard.soil_reinforcement_profile import (
    SoilReinforcementProfile,
)
from koswat.strategies.strategy_reinforcement_input import (
    FixedStrategyReinforcementInput,
    FlexibleStrategyReinforcementInput,
    StrategyReinforcementInputBase,
)
from koswat.strategies.strategy_reinforcement_type_costs import (
    ReinforcementProfileProtocol,
)


@dataclass
class StrategyReinforcementInputBuilder:
    """
    A builder for creating strategy reinforcement inputs.
    """

    reinforcement_type: type[ReinforcementProfileProtocol]
    active: bool
    base_costs_with_surtax: float
    ground_level_surface: float

    def build(self) -> StrategyReinforcementInputBase:
        if self.reinforcement_type is None:
            raise ValueError("Reinforcement type must be set before building.")

        if self.reinforcement_type is not SoilReinforcementProfile:
            return FlexibleStrategyReinforcementInput(
                reinforcement_type=self.reinforcement_type,
                active=self.active,
                base_costs_with_surtax=self.base_costs_with_surtax,
                ground_level_surface=self.ground_level_surface,
            )

        return FixedStrategyReinforcementInput(
            reinforcement_type=self.reinforcement_type,
            active=self.active,
            base_costs_with_surtax=self.base_costs_with_surtax,
            ground_level_surface=self.ground_level_surface,
        )
