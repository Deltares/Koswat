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

from koswat.dike_reinforcements.reinforcement_profile.reinforcement_profile_protocol import (
    ReinforcementProfileProtocol,
)
from typing import Callable, Any
from koswat.dike_reinforcements.reinforcement_profile.reinforcement_room_calculator.polderside_and_waterside_room_calculator import (
    PoldersideAndWatersideRoomCalculator,
)
from koswat.dike_reinforcements.reinforcement_profile.reinforcement_room_calculator.polderside_only_room_calculator import (
    PoldersideOnlyRoomCalculator,
)

# This file is aimed to contain all the shared logic that can be used to decorate the reinforcement profile classes.
# The decorators are used to add additional functionality to the reinforcement profile classes without modifying their original implementation.
# This removes the need of extra abstraction layers and allows for a more flexible and modular design.


def polder_and_waterside_room_calculator(
    func: Callable[[ReinforcementProfileProtocol, bool], Any],
) -> Callable[[ReinforcementProfileProtocol, bool], Any]:
    def wrapped(self, waterside_allowed: bool):
        if not waterside_allowed:
            return PoldersideOnlyRoomCalculator(
                required_polderside_width=self.polderside_width,
            )
        return PoldersideAndWatersideRoomCalculator(
            required_waterside_width=self.waterside_width,
            required_polderside_width=self.polderside_width,
        )

    return wrapped
