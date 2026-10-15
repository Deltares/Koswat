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

from koswat.strategies.criteria.strategy_reinforcement_active_filter_criteria import (
    StrategyReinforcementActiveFilterCriteria,
)
from koswat.strategies.criteria.strategy_reinforcement_widths_filter_criteria import (
    StrategyReinforcementWidthsFilterCriteria,
)
from koswat.strategies.order_strategy.criteria.order_strategy_reinforcement_filter_criteria import (
    OrderStrategyReinforcementFilterCriteria,
)
from koswat.strategies.strategy_input import StrategyInput
from koswat.strategies.strategy_reinforcement_filter_criteria_protocol import (
    StrategyReinforcementFilterCriteriaProtocol,
)
from koswat.strategies.strategy_reinforcement_input import (
    StrategyReinforcementInputProtocol,
)


class OrderStrategyReinforcementFiltering:
    """
    Verifies if a given `strategy_input` should be skipped based on its type and costs,
    in comparison with a collection of other strategies (`other_strategies`)
    """

    def __init__(self, strategy_input: StrategyInput) -> None:
        self.strategy_input = strategy_input
        self.prefilters: list[StrategyReinforcementFilterCriteriaProtocol] = [
            StrategyReinforcementActiveFilterCriteria(self.strategy_input),
            StrategyReinforcementWidthsFilterCriteria(self.strategy_input),
        ]

    def filter(
        self, strategy_reinforcements: list[StrategyReinforcementInputProtocol]
    ) -> list[StrategyReinforcementInputProtocol]:
        """
        Filters the given reinforcement profiles based on the collection criteria.
        Args:
            strategy_reinforcements (list[StrategyReinforcementInputProtocol]): The list of reinforcement profiles to filter.
        Returns:
            list[StrategyReinforcementInputProtocol]: List of reinforcement profiles that meet the collection criteria.
        """
        if not strategy_reinforcements:
            return []
        _eligible_strategies = list(
            filter(self._strategy_reinforcement_meets_criteria, strategy_reinforcements)
        )

        return list(
            filter(
                OrderStrategyReinforcementFilterCriteria(
                    _eligible_strategies
                ).criteria_met_by,
                _eligible_strategies,
            )
        )

    def _strategy_reinforcement_meets_criteria(
        self, strategy_reinforcement: StrategyReinforcementInputProtocol
    ) -> bool:
        return all(
            _criteria.criteria_met_by(strategy_reinforcement)
            for _criteria in self.prefilters
        )
