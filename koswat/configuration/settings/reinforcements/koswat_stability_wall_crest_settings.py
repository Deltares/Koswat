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

from dataclasses import dataclass
from typing import Any

from koswat.configuration.settings.reinforcements.koswat_stability_wall_toe_settings import (
    KoswatStabilityWallToeSettings,
)


@dataclass
class KoswatStabilityWallCrestSettings(KoswatStabilityWallToeSettings):
    """
    Settings related to Stability wall (crest) reinforcement
    """

    transition_sheetpile_diaphragm_wall: float = 99

    def set_defaults(
        self,
        other: "KoswatStabilityWallCrestSettings",
    ) -> "KoswatStabilityWallCrestSettings":
        """
        Add the defaults from another KoswatStabilityWallCrestSettings instance to this instance, if not set.

        Args:
            other (KoswatStabilityWallCrestSettings): The other instance to get defaults from.

        Raises:
            TypeError: If the other instance has a different type.

        Returns:
            KoswatStabilityWallCrestSettings: The instance with defaults set.
        """
        if not isinstance(other, KoswatStabilityWallCrestSettings):
            raise TypeError(
                "Can only merge with another KoswatStabilityWallCrestSettings instance."
            )

        super().set_defaults(other)

        def _set_default(this_value: Any, other_value: Any) -> Any:
            if this_value is None:
                return other_value
            return this_value

        self.transition_sheetpile_diaphragm_wall = _set_default(
            self.transition_sheetpile_diaphragm_wall,
            other.transition_sheetpile_diaphragm_wall,
        )

        return self
