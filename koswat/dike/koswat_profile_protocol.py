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

from typing import Optional, Protocol, runtime_checkable

from shapely.geometry.point import Point

from koswat.dike.characteristic_points.characteristic_points import CharacteristicPoints
from koswat.dike.koswat_input_profile_protocol import KoswatInputProfileProtocol
from koswat.dike.layers.layers_wrapper import KoswatLayersWrapper


@runtime_checkable
class KoswatProfileProtocol(Protocol):
    input_data: KoswatInputProfileProtocol
    characteristic_points: CharacteristicPoints
    layers_wrapper: KoswatLayersWrapper
    location: Optional[Point]
    points: list[Point]
    profile_width: float
    profile_height: float
