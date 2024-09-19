import math
from dataclasses import dataclass

from koswat.configuration.koswat_config_protocol import KoswatConfigProtocol


def _valid_float_prop(config_property: float) -> bool:
    return config_property is not None and not math.isnan(config_property)


@dataclass
class DikeProfileCostsSettings(KoswatConfigProtocol):
    added_layer_grass_m3: float = math.nan
    added_layer_clay_m3: float = math.nan
    added_layer_sand_m3: float = math.nan
    reused_layer_grass_m3: float = math.nan
    reused_layer_core_m3: float = math.nan
    disposed_material_m3: float = math.nan
    profiling_layer_grass_m2: float = math.nan
    profiling_layer_clay_m2: float = math.nan
    profiling_layer_sand_m2: float = math.nan
    bewerken_maaiveld_m2: float = math.nan

    def is_valid(self) -> bool:
        return all(_valid_float_prop(_prop) for _prop in self.__dict__.values())
