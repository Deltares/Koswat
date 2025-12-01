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
from dataclasses import dataclass, field

from koswat.dike.surroundings.koswat_surroundings_protocol import (
    KoswatSurroundingsProtocol,
)
from koswat.dike.surroundings.point.point_surroundings import PointSurroundings


@dataclass
class SurroundingsInfrastructure(KoswatSurroundingsProtocol):
    """
    Defines surroundings point collections that can be repaired or replaced.

    The `PointSurroundings` contain a matrix (dictionary) where the keys
    represent the distances to an obstacle, and the values a float representing
    how long that infrastructure is.
    """

    infrastructure_name: str = ""
    infrastructure_width: float = math.nan
    points: list[PointSurroundings] = field(default_factory=lambda: [])
