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


class StrategyWidthBoundaries:
    """
    Represents the width boundaries for a reinforcement input.
    """

    width_polderside: float = float("nan")
    width_waterside: float = float("nan")

    def within(self, other: "StrategyWidthBoundaries") -> bool:
        """
        Checks if the current width boundaries are within the specified other boundaries.

        Args:
            other (StrategyWidthBoundaries): The other width boundaries to compare against.

        Returns:
            bool: True if the current width boundaries are within the other boundaries, False otherwise.
        """
        if float.isnan(self.width_polderside) or float.isnan(self.width_waterside):
            return False

        if float.isnan(other.width_polderside):
            return self.width_polderside <= other.width_polderside
        if float.isnan(other.width_waterside):
            return self.width_waterside <= other.width_waterside
        return (
            self.width_polderside <= other.width_polderside
            and self.width_waterside <= other.width_waterside
        )
