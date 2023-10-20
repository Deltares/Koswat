from __future__ import annotations

import math
from typing import List, Tuple

from koswat.dike_reinforcements.reinforcement_profiles.reinforcement_profile_protocol import (
    ReinforcementProfileProtocol,
)
from koswat.cost_report.profile.volume_cost_parameters_calculator import (
    VolumeCostParametersCalculator,
)
from koswat.dike.material.koswat_material_type import KoswatMaterialType


class VolumeCostParameter:
    volume: float
    cost: float

    def total_cost(self) -> float:
        return self.volume * self.cost


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

    def get_parameters(self) -> List[VolumeCostParameter]:
        return list(
            filter(lambda x: isinstance(x, VolumeCostParameter), self.__dict__.values())
        )

    def get_material_total_volume_parameters(
        self, material_type: KoswatMaterialType
    ) -> Tuple[float, float]:
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

    @classmethod
    def from_reinforced_profile(
        cls, reinforced_profile: ReinforcementProfileProtocol
    ) -> VolumeCostParameters:
        """
        Generates a valid instance of `VolumeCostParameters` based on the provided instance of a `ReinforcementProfileProtocol`.

        Args:
            reinforced_profile (ReinforcementProfileProtocol): Instance containing the base information to be used.

        Returns:
            VolumeCostParameters: Instance with initialized valid parameters.
        """

        def _create(volume: float, cost: float) -> VolumeCostParameter:
            _vp = VolumeCostParameter()
            _vp.volume = volume
            _vp.cost = cost
            return _vp

        _volume_parameters = cls()
        _vcp = VolumeCostParametersCalculator.from_reinforced_profile(
            reinforced_profile
        )
        if not _vcp:
            return _volume_parameters
        _volume_parameters.reused_grass_volume = _create(
            _vcp.get_reused_grass_volume(), 6.04
        )
        _volume_parameters.aanleg_grass_volume = _create(
            _vcp.get_aanleg_grass_volume(), 12.44
        )
        _volume_parameters.aanleg_clay_volume = _create(
            _vcp.get_aanleg_clay_volume(), 18.05
        )
        _volume_parameters.reused_core_volume = _create(
            _vcp.get_reused_core_volume(), 4.67
        )
        _volume_parameters.aanleg_core_volume = _create(
            _vcp.get_aanleg_core_volume(), 10.98
        )
        _volume_parameters.removed_material_volume = _create(
            _vcp.get_removed_material_volume(), 7.07
        )
        _volume_parameters.new_grass_layer_surface = _create(
            _vcp.new_grass_layer_surface, 0.88
        )
        _volume_parameters.new_clay_layer_surface = _create(
            _vcp.new_clay_layer_surface, 0.65
        )
        _volume_parameters.new_core_layer_surface = _create(
            _vcp.new_core_layer_surface, 0.6
        )
        _volume_parameters.new_maaiveld_surface = _create(
            _vcp.new_maaiveld_surface, 0.25
        )
        return _volume_parameters
