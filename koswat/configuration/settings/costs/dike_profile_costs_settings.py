
import math

from koswat.configuration.koswat_config_protocol import KoswatConfigProtocol


def _valid_float_prop(config_property: float) -> bool:
    return config_property is not None and not math.isnan(config_property)


class DikeProfileCostsSettings(KoswatConfigProtocol):
    added_layer_grass_m3: float
    added_layer_clay_m3: float
    added_layer_sand_m3: float
    reused_layer_grass_m3: float
    reused_layer_core_m3: float
    disposed_material_m3: float
    profiling_layer_grass_m2: float
    profiling_layer_clay_m2: float
    profiling_layer_sand_m2: float
    bewerken_maaiveld_m2: float

    def __init__(self) -> None:
        self.added_layer_grass_m3 = math.nan
        self.added_layer_clay_m3 = math.nan
        self.added_layer_sand_m3 = math.nan
        self.reused_layer_grass_m3 = math.nan
        self.reused_layer_core_m3 = math.nan
        self.disposed_material_m3 = math.nan
        self.profiling_layer_grass_m2 = math.nan
        self.profiling_layer_clay_m2 = math.nan
        self.profiling_layer_sand_m2 = math.nan
        self.bewerken_maaiveld_m2 = math.nan

    def is_valid(self) -> bool:
        return all(_valid_float_prop(_prop) for _prop in self.__dict__.values())

