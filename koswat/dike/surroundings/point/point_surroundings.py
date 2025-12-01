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

from __future__ import annotations
import math
from dataclasses import dataclass, field

from shapely.geometry import Point


@dataclass
class PointSurroundings:
    """
    Object representing a `meter` with `x`, `y` coordinates in a polder (or else).
    """

    section: str = ""
    traject_order: int = -1
    location: Point | None = None
    surroundings_matrix: dict[float, float] = field(default_factory=dict)

    def __hash__(self) -> int:
        """
        Overriding of the "magic" hash operator required
        so that `PointSurroundings` can be used as a key in a python dict.
        """
        return hash(
            (
                self.section,
                self.traject_order,
                self.location,
            )
        )

    def __eq__(self, __value: object) -> bool:
        """
        Overriding of the "magic" equality operator required
        so that `PointSurroundings` can be used as a key in a python dict.
        """
        if not isinstance(__value, type(self)):
            return False
        return (self.location, self.section, self.traject_order) == (
            __value.location,
            __value.section,
            __value.traject_order,
        )

    def merge(self, other: PointSurroundings) -> None:
        """
        Merges another `PointSurroundings` into this one by updating the
        `surroundings_matrix` with the values from the other one.

        Args:
            other (PointSurroundings): The other `PointSurroundings` to merge.
        """

        for _s_key, _s_value in other.surroundings_matrix.items():
            if _s_key in self.surroundings_matrix:
                self.surroundings_matrix[_s_key] += _s_value
            else:
                self.surroundings_matrix[_s_key] = _s_value

    def get_total_infrastructure_per_zone(
        self, *zone_limit_collection: tuple[float, float]
    ) -> list[float]:
        """
        Gets the total infrastructure width at each of the provided zones
        `zone_limit_collection` (`tuple[float, float]`).
        The zone limits are matched by rounding up their upper limit to the
        `surroundings_matrix` keys (distances to the `location` in the real world).
        When two zones have overlapping limits (as expected) the lower one will
        "claim" the corresponding surrounding distance.

        Example:
            - `zone_limit_collection` = (0, 4), (4, 11)
            - `surroundings_matrix` = {5: 1.5, 10: 3, 15: 6}
            - "Taken" distances per zone:
                - `(0, 4)` takes key `5`.
                - `(4, 11)` takes key(s) `10` and `15` because `5` was already taken.
            - Total infrastructure width at zones = `(1.5, 9)`

        Returns:
            list[float]: list with total width corresponding to each provided zone.
        """

        # Prepare data.
        _sorted_matrix_array = sorted(
            self.surroundings_matrix.items(), key=lambda item: item[0]
        )

        _taken_keys = []

        def matrix_idx_for_limits(limits: tuple[float, float]) -> float:
            _lower_limit, _upper_limit = limits
            if math.isclose(_upper_limit, 0, abs_tol=1e-09):
                return 0
            _total_width = 0
            for _matrix_distance, value in _sorted_matrix_array:
                if _matrix_distance in _taken_keys or (
                    _matrix_distance < _lower_limit
                    and not math.isclose(_matrix_distance, _lower_limit)
                ):
                    continue

                _total_width += value
                if value != 0:
                    _taken_keys.append(_matrix_distance)
                if _matrix_distance > _upper_limit or math.isclose(
                    _matrix_distance, _upper_limit
                ):
                    # We include the first value above the `upper_limit`,
                    # then we stop. (Design decission taken with PO).
                    break
            return _total_width

        return list(map(matrix_idx_for_limits, zone_limit_collection))

