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

from koswat.dike_reinforcements.reinforcement_profile.outside_slope.cofferdam_reinforcement_profile import (
    CofferdamReinforcementProfile,
)
from koswat.strategies.criteria.strategy_reinforcement_allowed_waterside_filter_criteria import (
    StrategyReinforcementAllowedWatersideFilterCriteria,
)
from koswat.strategies.strategy_reinforcement_filter_criteria_protocol import (
    StrategyReinforcementFilterCriteriaProtocol,
)
from koswat.strategies.strategy_reinforcement_input import (
    StrategyReinforcementInputProtocol,
)


class StrategyReinforcementActiveFilterCriteria(
    StrategyReinforcementFilterCriteriaProtocol
):
    """
    This class is used to filter reinforcement profiles based on their active criteria.
    It allows only active reinforcements or those of type `CofferdamReinforcementProfile` to pass the filter.
    """

    def __init__(self, strategy_input) -> None:
        self._waterside_criteria = StrategyReinforcementAllowedWatersideFilterCriteria(
            strategy_input.waterside_reinforcement_allowed
        )

    def criteria_met_by(
        self, strategy_reinforcement: StrategyReinforcementInputProtocol
    ) -> bool:
        if not self._waterside_criteria.criteria_met_by(strategy_reinforcement):
            return False
        return (
            strategy_reinforcement.active
            or strategy_reinforcement.reinforcement_type
            == CofferdamReinforcementProfile
        )
