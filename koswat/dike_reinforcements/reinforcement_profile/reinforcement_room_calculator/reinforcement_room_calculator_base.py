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

from abc import ABC, abstractmethod
import math
from dataclasses import dataclass

from koswat.dike_reinforcements.reinforcement_profile.reinforcement_room_calculator.reinforcement_room_calculator_protocol import ReinforcementRoomCalculatorProtocol

@dataclass
class ReinforcementRoomCalculatorBase(ABC, ReinforcementRoomCalculatorProtocol):
    required_polderside_width: float
    required_waterside_width: float

    def _required_width_less_or_equal(self, a: float) -> bool:
        return self.required_width < a or math.isclose(a, self.required_width, rel_tol=1e-9)

    @property
    @abstractmethod
    def required_width(self) -> float:
        pass

    @abstractmethod
    def reinforcement_has_room(self, inside: float, outside: float) -> bool:
        """
        Checks if there is enough room for reinforcement between the inside and outside dimensions.

        Args:
            inside (float): The inside dimension.
            outside (float): The outside dimension.

        Returns:
            bool: True if there is enough room for reinforcement, False otherwise.
        """
        pass

