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

import math
from dataclasses import dataclass, field

from koswat.strategies.strategy_location_input import StrategyLocationInput
from koswat.strategies.strategy_reinforcement_input import StrategyReinforcementInput


@dataclass
class StrategyInput:
    """
    Represents the input data structure for a strategy.
    """

    strategy_locations: list[StrategyLocationInput] = field(default_factory=lambda: [])
    strategy_reinforcements: list[StrategyReinforcementInput] = field(
        default_factory=lambda: []
    )
    reinforcement_min_buffer: float = 0.0
    reinforcement_min_length: float = 0.0

    @property
    def reinforcement_min_cluster(self) -> int:
        """
        Returns the minimum length of a reinforcement type
        along a traject, usually named as `cluster` throughout
        the code.

        Returns:
            int: `Total length`
        """
        if math.isnan(self.reinforcement_min_buffer):
            return -1
        return int(round(2 * self.reinforcement_min_buffer)) + 1
