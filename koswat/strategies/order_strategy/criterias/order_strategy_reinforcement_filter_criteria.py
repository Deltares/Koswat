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
    StrategyReinforcementInputProtocol,
)
from koswat.dike_reinforcements.reinforcement_profile.outside_slope.cofferdam_reinforcement_profile import (
    CofferdamReinforcementProfile,
)


class OrderStrategyReinforcementFilterCriteria:
    """
    Verifies if a given `strategy_input` should be skipped based on its type and costs,
    in comparison with a collection of other strategies (`other_strategies`)
    """

    def __init__(
        self,
        strategies: list[StrategyReinforcementInputProtocol],
    ):
        self.strategies = strategies

    def filter(self) -> list[StrategyReinforcementInputProtocol]:
        """
        Filters the strategies based on their costs and types.

        Returns:
            list[StrategyReinforcementInputProtocol]: A list of strategies that are not skippable.
        """
        if not self.strategies:
            return []
        _chosen_strategies = []
        _eligible_strategies = list(
            filter(lambda x: self._is_eligible(x), self.strategies)
        )
        for _strategy in _eligible_strategies:
            if not self._is_comparable(_strategy) or self._is_optimal(
                _strategy, _eligible_strategies
            ):
                _chosen_strategies.append(_strategy)

        return _chosen_strategies

    def _is_eligible(self, strategy_input: StrategyReinforcementInputProtocol) -> bool:
        """
        Determines if a strategy reinforcement is active or otherwise type of Cofferdam.
        """
        # Cofferdam is always eligible, even if not active
        return (
            strategy_input.active
            or strategy_input.reinforcement_type == CofferdamReinforcementProfile
        )

    def _is_optimal(
        self,
        strategy: StrategyReinforcementInputProtocol,
        eligible_strategies: list[StrategyReinforcementInputProtocol],
    ) -> bool:
        """
        Determines if a strategy reinforcement meets the criteria to be considered for filtering.
        """
        if strategy.reinforcement_type == CofferdamReinforcementProfile:
            return True
        return not any(
            self._can_be_filtered_out_by(strategy, _other_strategy)
            for _other_strategy in eligible_strategies
            if _other_strategy != strategy
        )

    def _is_comparable(
        self, strategy_input: StrategyReinforcementInputProtocol
    ) -> bool:
        """
        Determine if a strategy reinforcement can be used to determine whether it should be skipped,
        or other strategies should be skipped in favor of this one.
        """
        return not isinstance(strategy_input, FixedStrategyReinforcementInput)

    def _can_be_filtered_out_by(
        self,
        strategy_input: StrategyReinforcementInputProtocol,
        strategy_to_compare: StrategyReinforcementInputProtocol,
    ) -> bool:
        """
        Compare the two strategies based on their total costs.
        """
        if not self._is_comparable(strategy_to_compare):
            return False
        return strategy_input.is_more_cost_space_restrictive(strategy_to_compare)
