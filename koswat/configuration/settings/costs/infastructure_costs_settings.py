import math

from koswat.configuration.koswat_config_protocol import KoswatConfigProtocol


def _valid_float_prop(config_property: float) -> bool:
    return config_property is not None and not math.isnan(config_property)

class InfrastructureCostsSettings(KoswatConfigProtocol):
    removing_roads_klasse2: float
    removing_roads_klasse24: float
    removing_roads_klasse47: float
    removing_roads_klasse7: float
    removing_roads_unknown: float
    adding_roads_klasse2: float
    adding_roads_klasse24: float
    adding_roads_klasse47: float
    adding_roads_klasse7: float
    adding_roads_unknown: float

    def __init__(self) -> None:
        self.removing_roads_klasse2 = math.nan
        self.removing_roads_klasse24 = math.nan
        self.removing_roads_klasse47 = math.nan
        self.removing_roads_klasse7 = math.nan
        self.removing_roads_unknown = math.nan
        self.adding_roads_klasse2 = math.nan
        self.adding_roads_klasse24 = math.nan
        self.adding_roads_klasse47 = math.nan
        self.adding_roads_klasse7 = math.nan
        self.adding_roads_unknown = math.nan

    def is_valid(self) -> bool:
        return all(_valid_float_prop(_prop) for _prop in self.__dict__.values())

