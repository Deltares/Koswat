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
from koswat.strategies.strategy_reinforcement_filter_criteria_protocol import (
    StrategyReinforcementFilterCriteriaProtocol,
)
from koswat.strategies.strategy_reinforcement_input import (
    StrategyReinforcementInputProtocol,
)
from koswat.strategies.strategy_reinforcement_input.fixed_strategy_reinforcement_input import (
    FixedStrategyReinforcementInput,
)


class OrderStrategyReinforcementFilterCriteria(
    StrategyReinforcementFilterCriteriaProtocol
):
    """
    This class is used to filter reinforcement profiles based on the order strategy criteria.
    """

    def __init__(
        self,
        strategy_reinforcements: list[StrategyReinforcementInputProtocol],
    ):
        self._strategy_reinforcements = strategy_reinforcements

    def meets_criteria(
        self, strategy_reinforcement: StrategyReinforcementInputProtocol
    ) -> bool:
        if (
            not self._is_comparable(strategy_reinforcement)
            or strategy_reinforcement.reinforcement_type
            == CofferdamReinforcementProfile
        ):
            return True

        return not any(
            self._can_be_filtered_out_by(strategy_reinforcement, _other_strategy)
            for _other_strategy in self._strategy_reinforcements
            if _other_strategy != strategy_reinforcement
        )

    def _can_be_filtered_out_by(
        self,
        strategy_reinforcement: StrategyReinforcementInputProtocol,
        strategy_reinforcement_to_compare: StrategyReinforcementInputProtocol,
    ) -> bool:
        """
        Compare the two strategies based on their total costs.
        """
        if not self._is_comparable(strategy_reinforcement_to_compare):
            return False
        return strategy_reinforcement.is_more_cost_space_restrictive(
            strategy_reinforcement_to_compare
        )

    def _is_comparable(
        self, strategy_reinforcement: StrategyReinforcementInputProtocol
    ) -> bool:
        return not isinstance(strategy_reinforcement, FixedStrategyReinforcementInput)
