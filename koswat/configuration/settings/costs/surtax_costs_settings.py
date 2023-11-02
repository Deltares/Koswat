import math

from koswat.configuration.koswat_config_protocol import KoswatConfigProtocol
from koswat.configuration.settings.koswat_general_settings import SurtaxFactorEnum


def _valid_float_prop(config_property: float) -> bool:
    return config_property is not None and not math.isnan(config_property)


class SurtaxCostsSettings(KoswatConfigProtocol):
    soil_easy: float
    soil_normal: float
    soil_hard: float
    construction_easy: float
    construction_normal: float
    construction_hard: float
    roads_easy: float
    roads_normal: float
    roads_hard: float
    land_purchase_easy: float
    land_purchase_normal: float
    land_purchase_hard: float

    def _get_surtax(
        self, surtax_type: str, surtax_factor: SurtaxFactorEnum | None
    ) -> float:
        if not surtax_factor:
            return 0
        if surtax_factor == SurtaxFactorEnum.MAKKELIJK:
            level = "easy"
        elif surtax_factor == SurtaxFactorEnum.NORMAAL:
            level = "normal"
        elif surtax_factor == SurtaxFactorEnum.MOEILIJK:
            level = "hard"
        return getattr(self, f"{surtax_type}_{level}")

    def get_soil_surtax(
        self,
        surtax_factor: SurtaxFactorEnum,
    ) -> float:
        return self._get_surtax("soil", surtax_factor)

    def get_constructive_surtax(
        self,
        surtax_factor: SurtaxFactorEnum | None,
    ) -> float:
        return self._get_surtax("construction", surtax_factor)

    def get_land_purchase_surtax(
        self,
        surtax_factor: SurtaxFactorEnum | None,
    ) -> float:
        return self._get_surtax("land_purchase", surtax_factor)

    def __init__(self) -> None:
        self.soil_easy = math.nan
        self.soil_normal = math.nan
        self.soil_hard = math.nan
        self.construction_easy = math.nan
        self.construction_normal = math.nan
        self.construction_hard = math.nan
        self.roads_easy = math.nan
        self.roads_normal = math.nan
        self.roads_hard = math.nan
        self.land_purchase_easy = math.nan
        self.land_purchase_normal = math.nan
        self.land_purchase_hard = math.nan

    def is_valid(self) -> bool:
        return all(_valid_float_prop(_prop) for _prop in self.__dict__.values())
