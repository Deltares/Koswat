"""
                    GNU GENERAL PUBLIC LICENSE
                      Version 3, 29 June 2007

    KOSWAT, from the dutch combination of words `Kosts-Wat` (what are the costs)
    Copyright (C) 2024 Stichting Deltares

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
from dataclasses import dataclass

from koswat.dike.koswat_profile_protocol import KoswatProfileProtocol
from koswat.dike_reinforcements.reinforcement_profile.reinforcement_profile_protocol import (
    ReinforcementProfileProtocol,
)


@dataclass
class ProfileZoneCalculator:
    """
    Calculator to determine the width of zones `A` and `B` of a reinforced
    profile (`ReinforcementProfileProtocol`). It requires its original base
    profile to be in its definition.
    """

    reinforced_profile: ReinforcementProfileProtocol

    def _get_profile_upper_x_coords(
        self, profile: KoswatProfileProtocol
    ) -> tuple[float, float]:
        _upper_x_coords = [
            _p.x for _p in profile.points if math.isclose(_p.y, profile.profile_height)
        ]
        return min(_upper_x_coords), max(_upper_x_coords)

    def _calculate_zone_a_and_b(self) -> tuple[float, float]:
        _left_limit, _right_limit = self._get_profile_upper_x_coords(
            self.reinforced_profile.old_profile
        )
        _zone_a = _right_limit - _left_limit
        _zone_b = self.reinforced_profile.points[-1].x - _right_limit
        return (_zone_a, _zone_b)

    def _calculate_zone_b(self) -> tuple[float, float]:
        _left_limit, _ = self._get_profile_upper_x_coords(
            self.reinforced_profile.old_profile
        )
        _zone_b = self.reinforced_profile.points[-1].x - _left_limit
        return (0, _zone_b)

    def calculate(self) -> tuple[float, float]:
        """
        Calculates the width of zones `A` and `B` for the defined instance of
        `ReinforcementProfileProtocol`. The calculation is as follows:
        - When `dh0` has not varied with respect to the base profile, then zones
        `A` and `B` are calculated.
        - When `dh0` has increased then only zone `B` is calculated.

        Returns:
            tuple[float, float]: Calculated zone `A` and `B` respectively.
        """
        if not self.reinforced_profile or not self.reinforced_profile.old_profile:
            return (math.nan, math.nan)

        _new_height = self.reinforced_profile.profile_height
        _old_height = self.reinforced_profile.old_profile.profile_height
        if _new_height > _old_height and not math.isclose(_new_height, _old_height):
            return self._calculate_zone_b()
        return self._calculate_zone_a_and_b()
