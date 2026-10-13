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
from koswat.strategies.criterias.strategy_reinforcement_active_filter_criteria import (
    StrategyReinforcementActiveFilterCriteria,
)
from koswat.strategies.criterias.strategy_reinforcement_comparable_filter_criteria import (
    StrategyReinforcementComparableFilterCriteria,
)
from koswat.strategies.criterias.strategy_reinforcement_width_boundaries_filter_criteria import (
    StrategyReinforcementWidthBoundariesFilterCriteria,
)
from koswat.strategies.strategy_input import StrategyInput
from koswat.strategies.strategy_reinforcement_input import (
    StrategyReinforcementInputProtocol,
)
from koswat.strategies.strategy_reinforcement_input.fixed_strategy_reinforcement_input import (
    FixedStrategyReinforcementInput,
)


class OrderStrategyReinforcementFilterCriteria:
    """
    Verifies if a given `strategy_input` should be skipped based on its type and costs,
    in comparison with a collection of other strategies (`other_strategies`)
    """

    def __init__(self, strategy_input: StrategyInput) -> None:
        self.strategy_input = strategy_input
        self.prefilters = [
            StrategyReinforcementActiveFilterCriteria(),
            StrategyReinforcementWidthBoundariesFilterCriteria(self.strategy_input),
        ]

    def filter(
        self, strategy_reinforcements: list[StrategyReinforcementInputProtocol]
    ) -> list[StrategyReinforcementInputProtocol]:
        """
        Filters the given reinforcement profiles based on the collection criteria.

        Returns:
            list[StrategyReinforcementInputProtocol]: List of reinforcement profiles that meet the collection criteria.
        """
        if not strategy_reinforcements:
            return []
        _eligible_strategies = [
            _reinforcement
            for _reinforcement in filter(
                self._strategy_reinforcement_meets_criteria, strategy_reinforcements
            )
        ]
        return [
            _strategy_reinforcement
            for _strategy_reinforcement in _eligible_strategies
            if self._is_optimal(_strategy_reinforcement, _eligible_strategies)
        ]

    def _strategy_reinforcement_meets_criteria(
        self, strategy_reinforcement: StrategyReinforcementInputProtocol
    ) -> bool:
        return all(
            _criteria.meets_criteria(strategy_reinforcement)
            for _criteria in self.prefilters
        )

    def _is_optimal(
        self,
        strategy_reinforcement: StrategyReinforcementInputProtocol,
        eligible_strategy_reinforcements: list[StrategyReinforcementInputProtocol],
    ) -> bool:
        """
        Determines if a strategy reinforcement meets the criteria to be considered for filtering.
        """
        if (
            not self._is_comparable(strategy_reinforcement)
            or strategy_reinforcement.reinforcement_type
            == CofferdamReinforcementProfile
        ):
            return True

        return not any(
            self._can_be_filtered_out_by(strategy_reinforcement, _other_strategy)
            for _other_strategy in eligible_strategy_reinforcements
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
