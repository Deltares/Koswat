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

from koswat.strategies.strategy_reinforcement_input import (
    FixedStrategyReinforcementInput,
    StrategyReinforcementInputBase,
)


class OrderStrategyReinforcementSkipCriteria:
    """
    Verifies if a given `strategy_input` should be skipped based on its type and costs,
    in comparison with a collection of other strategies (`other_strategies`)
    """

    def __init__(
        self,
        strategy_input: StrategyReinforcementInputBase,
        other_strategies: list[StrategyReinforcementInputBase],
    ):
        self.strategy_input = strategy_input
        self.other_strategies = other_strategies

    def skip_reinforcement(self) -> bool:
        """
        Determine if a strategy reinforcement can be skipped based on the other strategies.

        Returns:
            bool: True if the strategy reinforcement can be skipped, False otherwise.
        """
        if not self._is_comparable(self.strategy_input):
            return False

        return any(
            self._can_be_filtered_out_by(_other_strategy)
            for _other_strategy in self.other_strategies
        )

    def _is_comparable(self, strategy_input: StrategyReinforcementInputBase) -> bool:
        """
        Determine if a strategy reinforcement can be used to determine whether it should be skipped,
        or other strategies should be skipped in favor of this one.

        Returns:
            bool: True if the strategy reinforcement is comparable, False otherwise.
        """
        return not isinstance(strategy_input, FixedStrategyReinforcementInput)

    def _can_be_filtered_out_by(
        self,
        strategy_to_compare: StrategyReinforcementInputBase,
    ) -> bool:
        """
        Compare the two strategies based on their total costs.

        Returns:
            bool: True if `self.strategy_input` can be filtered out by `strategy_to_compare`, False otherwise.
        """
        if not self._is_comparable(strategy_to_compare):
            return False
        return self.strategy_input.is_more_cost_space_restrictive(strategy_to_compare)
