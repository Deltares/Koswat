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
from dataclasses import dataclass

from koswat.dike.koswat_profile_protocol import KoswatProfileProtocol
from koswat.dike_reinforcements.reinforcement_profile.reinforcement_profile_protocol import (
    ReinforcementProfileProtocol,
)


@dataclass(kw_only=True)
class ProfileZoneCalculator:
    """
    Calculator to determine the width of zones `A`, `B`, and `C` of a reinforced
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

    def _calculate_all_zones(self) -> tuple[float, float, float]:
        _old_left_limit, _old_right_limit = self._get_profile_upper_x_coords(
            self.reinforced_profile.old_profile
        )
        _zone_a = _old_left_limit - self.reinforced_profile.points[0].x
        _zone_b = _old_right_limit - _old_left_limit
        _zone_c = self.reinforced_profile.points[-1].x - _old_right_limit
        return (_zone_a, _zone_b, _zone_c)

    def _calculate_a_c_zones(self) -> tuple[float, float, float]:
        _zone_a, _zone_b, _zone_c = self._calculate_all_zones()
        _zone_c = _zone_b + _zone_c
        _zone_b = 0.0
        return (_zone_a, _zone_b, _zone_c)

    def calculate(self) -> tuple[float, float, float]:
        """
        Calculates the width of zones `A`, `B`, and `C` for the defined instance of
        `ReinforcementProfileProtocol`. The calculation is as follows:
        - When crest height has not increased with respect to the base profile, then zones
        `A`, `B`, and `C` are calculated.
        - When crest height has increased then only zone `A` and `C` are calculated.

        Returns:
            tuple[float, float, float]: Calculated zone `A`, `B`, and `C` respectively.
        """
        if not self.reinforced_profile or not self.reinforced_profile.old_profile:
            return (math.nan, math.nan, math.nan)

        _new_height = self.reinforced_profile.profile_height
        _old_height = self.reinforced_profile.old_profile.profile_height

        if _new_height > _old_height and not math.isclose(_new_height, _old_height):
            return self._calculate_a_c_zones()

        return self._calculate_all_zones()
