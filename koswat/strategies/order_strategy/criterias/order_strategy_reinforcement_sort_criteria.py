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

from koswat.dike_reinforcements.reinforcement_profile.outside_slope.cofferdam_reinforcement_profile import (
    CofferdamReinforcementProfile,
)
from koswat.dike_reinforcements.reinforcement_profile.standard.soil_reinforcement_profile import (
    SoilReinforcementProfile,
)
from koswat.strategies.strategy_reinforcement_input import (
    StrategyReinforcementInputProtocol,
)


class OrderStrategyReinforcementSortCriteria:
    """
    Orders a list of strategy reinforcements based on the criteria from
    `OrderStrategyReinforcementFilterCriteria`
    """

    def __init__(
        self, strategy_reinforcements: list[StrategyReinforcementInputProtocol]
    ):
        self.strategy_reinforcements = strategy_reinforcements

    def sort(self) -> list[StrategyReinforcementInputProtocol]:
        """
        Sorts the strategy reinforcements input based on their descending ground level surface
        and associated costs.
        """
        # Get the eligible strategies based on the skip criteria
        if not self.strategy_reinforcements:
            return []

        # SoilReinforcement, if active
        _reinforcement_as_head = (
            self.strategy_reinforcements[0].reinforcement_type
            == SoilReinforcementProfile
        )

        # Cofferdam, if present
        _reinforcement_as_tail = (
            self.strategy_reinforcements[-1].reinforcement_type
            == CofferdamReinforcementProfile
        )

        # Always skip from sorting the last item (Cofferdam).
        _list_to_sort = (
            self.strategy_reinforcements[1:]
            if _reinforcement_as_head
            else self.strategy_reinforcements
        )
        _list_to_sort = _list_to_sort[:-1] if _reinforcement_as_tail else _list_to_sort

        _sorted_list = sorted(
            _list_to_sort,
            key=lambda x: (x.ground_level_surface, x.base_costs_with_surtax),
            reverse=True,
        )

        # Reappend the first and last items to the sorted list, if applicable
        if _reinforcement_as_head:
            _sorted_list.insert(0, self.strategy_reinforcements[0])
        if _reinforcement_as_tail:
            _sorted_list.append(self.strategy_reinforcements[-1])

        return _sorted_list
