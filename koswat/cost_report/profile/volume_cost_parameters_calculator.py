from koswat.configuration.settings.koswat_general_settings import ConstructionTypeEnum


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
    construction_length: float
    construction_type: ConstructionTypeEnum | None

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
