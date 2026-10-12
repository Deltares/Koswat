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

from koswat.strategies.strategy_reinforcement_input.strategy_reinforcement_input_protocol import (
    StrategyReinforcementInputProtocol,
)
from typing import Protocol


class StrategyReinforcementFilterCriteriaProtocol(Protocol):
    def filter(
        self, strategy_reinforcements: list[StrategyReinforcementInputProtocol]
    ) -> list[StrategyReinforcementInputProtocol]:
        """
        Filters the given reinforcement profiles based on the surroundings criteria.

        Returns:
            list[StrategyReinforcementInputProtocol]: List of reinforcement profiles that meet the surroundings criteria.
        """
