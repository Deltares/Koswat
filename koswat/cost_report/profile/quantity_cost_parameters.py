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
from typing import Protocol, runtime_checkable

from koswat.configuration.settings.costs.construction_costs_settings import (
    ConstructionFactors,
)
from koswat.dike.material.koswat_material_type import KoswatMaterialType


@runtime_checkable
class CostParameterProtocol(Protocol):
    surtax: float
    quantity: float

    @property
    def total_cost(self) -> float:
        """
        The total cost (quantity * unit cost)
        """
        pass

    @property
    def total_cost_with_surtax(self) -> float:
        """
        The total cost including surtaxes
        """
        pass


class SoilCostParameter(CostParameterProtocol):
    surtax: float
    quantity: float
    cost: float

    @property
    def total_cost(self) -> float:
        return self.quantity * self.cost

    @property
    def total_cost_with_surtax(self) -> float:
        return self.total_cost * self.surtax


class ConstructionCostParameter(CostParameterProtocol):
    surtax: float
    quantity: float
    factors: ConstructionFactors | None

    @property
    def total_cost(self) -> float:
        if not self.factors:
            return 0
        # Applied formula: f(x) = cx^2 + dx + z + f*x^g
        return (
            self.factors.c_factor * pow(self.quantity, 2)
            + self.factors.d_factor * self.quantity
            + self.factors.z_factor
            + self.factors.f_factor * pow(self.quantity, self.factors.g_factor)
        )

    @property
    def total_cost_with_surtax(self) -> float:
        return self.total_cost * self.surtax


class QuantityCostParameters:
    new_grass_volume: CostParameterProtocol
    new_clay_volume: CostParameterProtocol
    new_core_volume: CostParameterProtocol
    reused_grass_volume: CostParameterProtocol
    reused_core_volume: CostParameterProtocol
    removed_material_volume: CostParameterProtocol
    new_grass_layer_surface: CostParameterProtocol
    new_clay_layer_surface: CostParameterProtocol
    new_core_layer_surface: CostParameterProtocol
    new_ground_level_surface: CostParameterProtocol
    land_purchase_surface: CostParameterProtocol
    construction_length: CostParameterProtocol

    def __init__(self) -> None:
        self.new_grass_volume = None
        self.new_clay_volume = None
        self.new_core_volume = None
        self.reused_grass_volume = None
        self.reused_core_volume = None
        self.removed_material_volume = None
        self.new_grass_layer_surface = None
        self.new_clay_layer_surface = None
        self.new_core_layer_surface = None
        self.new_ground_level_surface = None
        self.land_purchase_surface = None
        self.construction_length = None

    def get_parameters(self) -> list[CostParameterProtocol]:
        return list(
            filter(
                lambda x: isinstance(x, CostParameterProtocol),
                self.__dict__.values(),
            )
        )

    def get_material_total_quantity_parameters(
        self, material_type: KoswatMaterialType
    ) -> tuple[float, float]:
        if material_type == KoswatMaterialType.SAND:
            if not self.new_core_volume:
                return math.nan, math.nan
            return (
                self.new_core_volume.total_cost,
                self.new_core_volume.total_cost_with_surtax,
            )
        if material_type == KoswatMaterialType.CLAY:
            if not self.new_clay_volume:
                return math.nan, math.nan
            return (
                self.new_clay_volume.total_cost,
                self.new_clay_volume.total_cost_with_surtax,
            )
        if material_type == KoswatMaterialType.GRASS:
            if not self.new_grass_volume:
                return math.nan, math.nan
            return (
                self.new_grass_volume.total_cost,
                self.new_grass_volume.total_cost_with_surtax,
            )
        raise ValueError(
            "Material {} currently not supported.".format(
                material_type.name.capitalize()
            )
        )
