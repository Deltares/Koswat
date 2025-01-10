import math
from dataclasses import dataclass

from koswat.configuration.koswat_config_protocol import KoswatConfigProtocol


def _valid_float_prop(config_property: float) -> bool:
    return config_property is not None and not math.isnan(config_property)


@dataclass
class InfrastructureCostsSettings(KoswatConfigProtocol):
    removing_roads_klasse2: float = math.nan
    removing_roads_klasse24: float = math.nan
    removing_roads_klasse47: float = math.nan
    removing_roads_klasse7: float = math.nan
    removing_roads_unknown: float = math.nan
    adding_roads_klasse2: float = math.nan
    adding_roads_klasse24: float = math.nan
    adding_roads_klasse47: float = math.nan
    adding_roads_klasse7: float = math.nan
    adding_roads_unknown: float = math.nan

    def is_valid(self) -> bool:
        return all(_valid_float_prop(_prop) for _prop in self.__dict__.values())
