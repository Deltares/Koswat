from __future__ import annotations

from koswat.calculations.reinforcement_profile_protocol import (
    ReinforcementProfileProtocol,
)


class VolumeCostParametersCalculator:
    grass_layer_removal_volume: float
    clay_layer_removal_volume: float
    new_core_layer_volume: float
    new_core_layer_surface: float
    new_clay_layer_volume: float
    new_clay_layer_surface: float
    new_grass_layer_volume: float
    new_grass_layer_surface: float
    new_maaiveld_surface: float

    @classmethod
    def from_reinforced_profile(
        cls, reinforced_profile: ReinforcementProfileProtocol
    ) -> VolumeCostParametersCalculator:
        _vcp = cls()
        if len(reinforced_profile.layers_wrapper.layers) != 3:
            return _vcp
        _grass_layer = reinforced_profile.layers_wrapper.get_layer("gras")
        _clay_layer = reinforced_profile.layers_wrapper.get_layer("klei")
        _core_layer = reinforced_profile.layers_wrapper.base_layer
        _vcp.grass_layer_removal_volume = _grass_layer.removal_layer_geometry.area
        _vcp.clay_layer_removal_volume = _clay_layer.removal_layer_geometry.area
        _vcp.new_core_layer_volume = _core_layer.new_layer_geometry.area
        _vcp.new_core_layer_surface = _core_layer.new_layer_surface.length
        _vcp.new_clay_layer_volume = _clay_layer.new_layer_geometry.area
        _vcp.new_clay_layer_surface = _clay_layer.new_layer_surface.length
        _vcp.new_grass_layer_volume = _grass_layer.new_layer_geometry.area
        _vcp.new_grass_layer_surface = _grass_layer.new_layer_surface.length
        _vcp.new_maaiveld_surface = reinforced_profile.new_ground_level_surface
        return _vcp

    def get_reused_grass_volume(self) -> float:
        return min(self.grass_layer_removal_volume, self.new_grass_layer_volume)

    def get_aanleg_grass_volume(self) -> float:
        return max(self.new_grass_layer_volume - self.grass_layer_removal_volume, 0)

    def get_aanleg_clay_volume(self) -> float:
        return self.new_clay_layer_volume

    def get_reused_core_volume(self) -> float:
        return min(self.clay_layer_removal_volume, self.new_core_layer_volume)

    def get_aanleg_core_volume(self) -> float:
        return max(self.new_core_layer_volume - self.clay_layer_removal_volume, 0)

    def get_removed_material_volume(self) -> float:
        _left_side = max(
            self.grass_layer_removal_volume - self.new_grass_layer_volume, 0
        )
        _right_side = max(
            self.clay_layer_removal_volume - self.new_core_layer_volume, 0
        )
        return _left_side + _right_side
