from __future__ import annotations

import math

from koswat.configuration.settings.costs.construction_costs_settings import (
    ConstructionFactors,
)
from koswat.dike.material.koswat_material_type import KoswatMaterialType


class VolumeCostParameter:
    volume: float
    cost: float

    def total_cost(self) -> float:
        return self.volume * self.cost


class LengthCostParameter:
    # TODO rename volume to quantity
    volume: float
    factors: ConstructionFactors | None

    def total_cost(self) -> float:
        if not self.factors:
            return 0
        # f(x) = cx^2 + dx + z + f*x^g
        return (
            self.factors.c_factor * pow(self.volume, 2)
            + self.factors.d_factor * self.volume
            + self.factors.z_factor
            + self.factors.f_factor * pow(self.volume, self.factors.g_factor)
        )


class VolumeCostParameters:
    reused_grass_volume: VolumeCostParameter
    aanleg_grass_volume: VolumeCostParameter
    aanleg_clay_volume: VolumeCostParameter
    reused_core_volume: VolumeCostParameter
    aanleg_core_volume: VolumeCostParameter
    removed_material_volume: VolumeCostParameter
    new_grass_layer_surface: VolumeCostParameter
    new_clay_layer_surface: VolumeCostParameter
    new_core_layer_surface: VolumeCostParameter
    new_maaiveld_surface: VolumeCostParameter
    construction_length: LengthCostParameter

    def __init__(self) -> None:
        self.reused_grass_volume = None
        self.aanleg_grass_volume = None
        self.aanleg_clay_volume = None
        self.reused_core_volume = None
        self.aanleg_core_volume = None
        self.removed_material_volume = None
        self.new_grass_layer_surface = None
        self.new_clay_layer_surface = None
        self.new_core_layer_surface = None
        self.new_maaiveld_surface = None
        self.construction_length = None

    def get_parameters(self) -> list[VolumeCostParameter | LengthCostParameter]:
        return list(
            filter(
                lambda x: isinstance(x, VolumeCostParameter | LengthCostParameter),
                self.__dict__.values(),
            )
        )

    def get_material_total_volume_parameters(
        self, material_type: KoswatMaterialType
    ) -> tuple[float, float]:
        if material_type == KoswatMaterialType.SAND:
            if not self.aanleg_core_volume:
                return math.nan, math.nan
            return self.aanleg_core_volume.volume, self.aanleg_core_volume.total_cost
        elif material_type == KoswatMaterialType.CLAY:
            if not self.aanleg_clay_volume:
                return math.nan, math.nan
            return self.aanleg_clay_volume.volume, self.aanleg_clay_volume.total_cost
        elif material_type == KoswatMaterialType.GRASS:
            if not self.aanleg_grass_volume:
                return math.nan, math.nan
            return self.aanleg_grass_volume.volume, self.aanleg_grass_volume.total_cost
        else:
            raise ValueError(
                "Material {} currently not supported.".format(
                    material_type.name.capitalize()
                )
            )
