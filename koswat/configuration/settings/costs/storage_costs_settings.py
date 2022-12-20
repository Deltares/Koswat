import math

from koswat.configuration.koswat_config_protocol import KoswatConfigProtocol


def _valid_float_prop(config_property: float) -> bool:
    return config_property is not None and not math.isnan(config_property)


class StorageCostsSettings(KoswatConfigProtocol):
    ground_easy: float
    ground_normal: float
    ground_hard: float
    construction_easy: float
    construction_normal: float
    construction_hard: float
    roads_easy: float
    roads_normal: float
    roads_hard: float
    ground_purchase_easy: float
    ground_purchase_normal: float
    ground_purchas_hard: float

    def __init__(self) -> None:
        self.ground_easy = math.nan
        self.ground_normal = math.nan
        self.ground_hard = math.nan
        self.construction_easy = math.nan
        self.construction_normal = math.nan
        self.construction_hard = math.nan
        self.roads_easy = math.nan
        self.roads_normal = math.nan
        self.roads_hard = math.nan
        self.ground_purchase_easy = math.nan
        self.ground_purchase_normal = math.nan
        self.ground_purchas_hard = math.nan

    def is_valid(self) -> bool:
        return all(_valid_float_prop(_prop) for _prop in self.__dict__.values())
