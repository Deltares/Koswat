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

from typing import Protocol, runtime_checkable

from shapely import geometry

from koswat.dike.material.koswat_material_type import KoswatMaterialType


@runtime_checkable
class KoswatLayerProtocol(Protocol):
    material_type: KoswatMaterialType
    upper_points: geometry.LineString
    outer_geometry: geometry.Polygon
    material_geometry: geometry.Polygon

    def as_data_dict(self) -> dict:
        """
        Returns the information related to an instance of the `KoswatLayerProtocol`.

        Returns:
            dict: custom dictionary with the relevant data.
        """
        pass
