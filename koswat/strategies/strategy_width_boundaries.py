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
from math import isnan
import re
from koswat.dike.koswat_profile_protocol import KoswatProfileProtocol


@dataclass(kw_only=True)
class StrategyWidthBoundaries:
    """
    Represents the width boundaries for a reinforcement input.
    """

    width_polderside: float = float("nan")
    width_waterside: float = float("nan")

    @classmethod
    def from_profile(cls, profile: KoswatProfileProtocol) -> "StrategyWidthBoundaries":
        """
        Creates a `StrategyWidthBoundaries` instance from a profile.

        Args:
            profile: The profile to extract width boundaries from.

        Returns:
            StrategyWidthBoundaries: An instance with the extracted width boundaries.
        """
        return cls(
            width_polderside=profile.width_polderside,
            width_waterside=profile.width_waterside,
        )

    def within(self, other: "StrategyWidthBoundaries") -> bool:
        """
        Checks if the current width boundaries are within the specified other boundaries.

        Args:
            other (StrategyWidthBoundaries): The other width boundaries to compare against.

        Returns:
            bool: True if the current width boundaries are within the other boundaries, False otherwise.
        """

        def _compare_widths(this: float, other: float) -> bool:
            if isnan(this):
                return False
            if isnan(other):
                return True
            return this <= other

        return _compare_widths(
            self.width_polderside, other.width_polderside
        ) and _compare_widths(self.width_waterside, other.width_waterside)
