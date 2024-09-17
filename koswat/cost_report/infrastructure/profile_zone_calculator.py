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
        _zone_a = abs(_right_limit - _left_limit)
        _zone_b = abs(self.reinforced_profile.points[-1].x - _right_limit)
        return (_zone_a, _zone_b)

    def _calculate_zone_b(self) -> tuple[float, float]:
        _left_limit, _ = self._get_profile_upper_x_coords(
            self.reinforced_profile.old_profile
        )
        _b_length = self.reinforced_profile.points[-1].x - _left_limit
        return (math.nan, _b_length)

    def calculate(self) -> tuple[float, float]:
        """
        Calculates the width of zones `A` and `B` for the defined instance of
        `ReinforcementProfileProtocol`. The calculation is as follows:
        - When `dh0` has not varied in respect to the base profile, then zones
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
