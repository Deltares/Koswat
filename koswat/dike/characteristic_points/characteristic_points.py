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

from dataclasses import dataclass

from shapely.geometry import Point


@dataclass
class CharacteristicPoints:
    p_1: Point = None
    p_2: Point = None
    p_3: Point = None
    p_4: Point = None
    p_5: Point = None
    p_6: Point = None
    p_7: Point = None
    p_8: Point = None

    @property
    def waterside(self) -> list[Point]:
        return [
            self.p_1,
            self.p_2,
            self.p_3,
            self.p_4,
        ]

    @waterside.setter
    def waterside(self, points: list[Point]):
        if not points or len(points) != 4:
            raise ValueError("Exactly 4 points should be given")
        if not all(isinstance(p, Point) for p in points):
            raise ValueError(f"All points given should be of type {type(Point)}")

        self.p_1 = points[0]
        self.p_2 = points[1]
        self.p_3 = points[2]
        self.p_4 = points[3]

    @property
    def polderside(self) -> list[Point]:
        return [
            self.p_5,
            self.p_6,
            self.p_7,
            self.p_8,
        ]

    @polderside.setter
    def polderside(self, points: list[Point]):
        if not points or len(points) != 4:
            raise ValueError("Exactly 4 points should be given")
        if not all(isinstance(p, Point) for p in points):
            raise ValueError(f"All points given should be of type {type(Point)}")

        self.p_5 = points[0]
        self.p_6 = points[1]
        self.p_7 = points[2]
        self.p_8 = points[3]

    @property
    def points(self) -> list[Point]:
        _points = []
        _points.extend(self.waterside)
        _points.extend(self.polderside)
        return _points

    @property
    def points_data(self) -> list[tuple[float]]:
        return [(p.x, p.y) for p in self.points]
