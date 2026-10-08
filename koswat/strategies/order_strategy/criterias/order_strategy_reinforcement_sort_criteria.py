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

from typing import Iterator

from koswat.strategies.order_strategy.criterias.order_strategy_reinforcement_filter_criteria import (
    OrderStrategyReinforcementSkipCriteria,
)
from koswat.strategies.strategy_reinforcement_input.strategy_reinforcement_input import (
    StrategyReinforcementInputBase,
)


class OrderStrategyReinforcementSortCriteria:
    """
    Orders a list of strategy reinforcements based on the criteria from
    `OrderStrategyReinforcementSkipCriteria`
    """

    def __init__(self, strategy_reinforcements: list[StrategyReinforcementInputBase]):
        self.strategy_reinforcements = strategy_reinforcements

    def sort(self) -> list[StrategyReinforcementInputBase]:
        _initial_sorting = self._initial_sort()
        return list(self._get_most_flexible_reinforcements(_initial_sorting))

    def _initial_sort(self) -> list[StrategyReinforcementInputBase]:
        return sorted(
            self.strategy_reinforcements,
            key=lambda x: (x.ground_level_surface, x.base_costs_with_surtax),
            reverse=True,
        )

    def _get_most_flexible_reinforcements(
        self,
        reinforcements: list[StrategyReinforcementInputBase],
    ) -> Iterator[StrategyReinforcementInputBase]:
        for _idx, _reinforcement in enumerate(reinforcements[:-1]):
            _skip_criteria = OrderStrategyReinforcementSkipCriteria(
                _reinforcement, reinforcements[_idx + 1 :]
            )
            if not _skip_criteria.skip_reinforcement():
                yield _reinforcement
        # Last reinforcement is always included,
        # as it is the least restrictive but most expensive
        yield reinforcements[-1]
