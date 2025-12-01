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
from typing import List

from shapely.geometry.point import Point

from koswat.core.protocols import BuilderProtocol
from koswat.dike.characteristic_points.characteristic_points import CharacteristicPoints
from koswat.dike.koswat_input_profile_protocol import KoswatInputProfileProtocol


class CharacteristicPointsBuilder(BuilderProtocol):
    input_profile: KoswatInputProfileProtocol
    p4_x_coordinate: float

    def __init__(self) -> None:
        self.input_profile = None
        self.p4_x_coordinate = math.nan

    def _build_waterside(self, p4_x: float) -> List[Point]:
        _p4 = Point(p4_x, self.input_profile.crest_height)
        _p3_x = _p4.x - (
            (self.input_profile.crest_height - self.input_profile.waterside_berm_height)
            * self.input_profile.waterside_slope
        )
        _p3 = Point(_p3_x, self.input_profile.waterside_berm_height)
        _p2_x = _p3.x - self.input_profile.waterside_berm_width
        _p2 = Point(_p2_x, self.input_profile.waterside_berm_height)
        _p1_x = _p2.x - (
            (
                self.input_profile.waterside_berm_height
                - self.input_profile.waterside_ground_level
            )
            * self.input_profile.waterside_slope
        )
        _p1 = Point(_p1_x, self.input_profile.waterside_ground_level)
        return [_p1, _p2, _p3, _p4]

    def _build_polderside(self, p4_x: float) -> List[Point]:
        _x_p5 = p4_x + self.input_profile.crest_width
        _p5 = Point(_x_p5, self.input_profile.crest_height)
        _x_p6 = _p5.x + (
            (
                self.input_profile.crest_height
                - self.input_profile.polderside_berm_height
            )
            * self.input_profile.polderside_slope
        )
        _p6 = Point(_x_p6, self.input_profile.polderside_berm_height)
        _x_p7 = _p6.x + self.input_profile.polderside_berm_width
        _p7 = Point(_x_p7, self.input_profile.polderside_berm_height)
        _x_p8 = _p7.x + (
            (
                self.input_profile.polderside_berm_height
                - self.input_profile.polderside_ground_level
            )
            * self.input_profile.polderside_slope
        )
        _p8 = Point(_x_p8, self.input_profile.polderside_ground_level)
        return [_p5, _p6, _p7, _p8]

    def build(self) -> CharacteristicPoints:
        if not self.input_profile:
            raise ValueError("Input Profile should be provided.")
        if math.isnan(self.p4_x_coordinate):
            self.p4_x_coordinate = 0

        _char_points = CharacteristicPoints()
        _char_points.waterside = self._build_waterside(self.p4_x_coordinate)
        _char_points.polderside = self._build_polderside(_char_points.p_4.x)
        return _char_points
