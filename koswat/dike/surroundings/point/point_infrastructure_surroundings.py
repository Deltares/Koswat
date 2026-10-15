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

from dataclasses import dataclass, field

from shapely.geometry import Point

from .point_surroundings_protocol import PointSurroundingsProtocol


@dataclass(kw_only=True)
class PointInfrastructureSurroundings(PointSurroundingsProtocol):
    """
    Object representing a `meter` with `x`, `y` coordinates in a polder (or else),
    extended with infrastructure specific properties.
    """

    section: str = ""
    traject_order: int = -1
    location: Point | None = None

    imported_surroundings: dict[float, float] = field(default_factory=dict)
    polderside_surroundings: dict[float, float] = field(default_factory=dict)
    waterside_surroundings: dict[float, float] = field(default_factory=dict)

    def __hash__(self) -> int:
        """
        Overriding of the "magic" hash operator required
        so that `PointInfrastructureSurroundings` can be used as a key in a python dict.
        """
        return hash(self.traject_order)

    def __eq__(self, value: object) -> bool:
        """
        Overriding of the "magic" equality operator required
        so that `PointInfrastructureSurroundings` can be used as a key in a python dict.
        """
        if not isinstance(value, type(self)):
            return False
        return self.traject_order == value.traject_order

    def merge(self, other: PointSurroundingsProtocol) -> None:
        if not isinstance(other, PointSurroundingsProtocol):
            raise TypeError(
                f"Expected an instance of PointSurroundingsProtocol, got {type(other)}"
            )

        self.polderside_surroundings = self.imported_surroundings
        self.waterside_surroundings = other.imported_surroundings

    def _get_infrastructure_width(
        self,
        taken_keys: list[float],
        limits: tuple[float, float],
        surroundings_array: list[tuple[float, float]],
    ) -> float:
        _lower_limit, _upper_limit = limits
        _total_width = 0.0
        for _matrix_distance, value in surroundings_array:
            if _matrix_distance in taken_keys:
                if _matrix_distance >= _upper_limit:
                    break
                continue

            if _matrix_distance < _lower_limit:
                continue

            if value != 0:
                _total_width += value
                taken_keys.append(_matrix_distance)

            if _matrix_distance >= _upper_limit:
                # We include the first value above the `upper_limit`,
                # then we stop. (Design decission taken with PO).
                break
        return _total_width

    def get_total_infrastructure_per_zone(
        self, *zone_limit_collection: tuple[float, float]
    ) -> list[float]:
        """
        Gets the total infrastructure length at each of the provided zones
        `zone_limit_collection` (`tuple[float, float, float]`).
        The zone limits are matched by rounding up their upper limit to the
        `polderside_surroundings` and `waterside_surroundings` keys
        (distances to the `location` in the real world).
        When two zones have overlapping limits (as expected) the lower one will
        "claim" the corresponding surrounding distance.

        Example:
            - `zone_limit_collection` = (-6, 0), (0, 4), (4, 11)
            - `polderside_surroundings` = {5: 1.5, 10: 3.0, 15: 6.0}
            - `waterside_surroundings` = {5: 2.0, 10: 4.0, 15: 8.0}
            - "Taken" distances per zone:
                - `(-6, 0)` takes waterside key `5` and `10`.
                - `(0, 4)` takes poldeside key `5`.
                - `(4, 11)` takes polderside keys `10` and `15` because `5` was already taken.
            - Total infrastructure width at zones = `(6.0, 1.5, 9.0)`

        Returns:
            list[float]: list with total length corresponding to each provided zone.
        """

        # Prepare data.
        _sorted_polderside_array = sorted(
            self.polderside_surroundings.items(), key=lambda item: item[0]
        )
        _sorted_waterside_array = sorted(
            self.waterside_surroundings.items(), key=lambda item: item[0]
        )

        _taken_polderside_keys: list[float] = []
        _taken_waterside_keys: list[float] = []

        def get_waterside_limits(limits: tuple[float, float]) -> tuple[float, float]:
            # change order and revert sign to make the limits positive for waterside calculations
            _upper_limit, _lower_limit = limits
            _lower_limit = max(-_lower_limit, 0)
            _upper_limit = max(-_upper_limit, 0)
            return _lower_limit, _upper_limit

        def get_polderside_limits(limits: tuple[float, float]) -> tuple[float, float]:
            _lower_limit, _upper_limit = limits
            _lower_limit = max(_lower_limit, 0)
            _upper_limit = max(_upper_limit, 0)
            return _lower_limit, _upper_limit

        def matrix_idx_for_limits(limits: tuple[float, float]) -> float:
            _total_infrastructure_width = 0.0

            _waterside_limits = get_waterside_limits(limits)
            if sum(_waterside_limits) > 0:
                _total_infrastructure_width += self._get_infrastructure_width(
                    _taken_waterside_keys, _waterside_limits, _sorted_waterside_array
                )

            _polderside_limits = get_polderside_limits(limits)
            if sum(_polderside_limits) > 0:
                _total_infrastructure_width += self._get_infrastructure_width(
                    _taken_polderside_keys, _polderside_limits, _sorted_polderside_array
                )

            return _total_infrastructure_width

        # Calculate zone A last for correct priority handling
        _zone_b_length = matrix_idx_for_limits(zone_limit_collection[1])
        _zone_c_length = matrix_idx_for_limits(zone_limit_collection[2])
        _zone_a_length = matrix_idx_for_limits(zone_limit_collection[0])

        return [_zone_a_length, _zone_b_length, _zone_c_length]
