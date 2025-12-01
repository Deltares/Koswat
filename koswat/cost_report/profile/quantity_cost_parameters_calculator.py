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

from koswat.configuration.settings.koswat_general_settings import ConstructionTypeEnum


class QuantityCostParametersCalculator:
    grass_layer_removal_volume: float
    clay_layer_removal_volume: float
    new_core_layer_volume: float
    new_core_layer_surface: float
    new_clay_layer_volume: float
    new_clay_layer_surface: float
    new_grass_layer_volume: float
    new_grass_layer_surface: float
    new_ground_level_surface: float
    construction_length: float
    construction_type: ConstructionTypeEnum | None

    def get_reused_grass_volume(self) -> float:
        return min(self.grass_layer_removal_volume, self.new_grass_layer_volume)

    def get_construction_grass_volume(self) -> float:
        return max(self.new_grass_layer_volume - self.grass_layer_removal_volume, 0)

    def get_construction_clay_volume(self) -> float:
        return self.new_clay_layer_volume

    def get_reused_core_volume(self) -> float:
        return min(self.clay_layer_removal_volume, self.new_core_layer_volume)

    def get_construction_core_volume(self) -> float:
        return max(self.new_core_layer_volume - self.clay_layer_removal_volume, 0)

    def get_removed_material_volume(self) -> float:
        _left_side = max(
            self.grass_layer_removal_volume - self.new_grass_layer_volume, 0
        )
        _right_side = max(
            self.clay_layer_removal_volume - self.new_core_layer_volume, 0
        )
        return _left_side + _right_side
