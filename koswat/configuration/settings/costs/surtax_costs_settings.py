import math
from dataclasses import dataclass

from koswat.configuration.koswat_config_protocol import KoswatConfigProtocol
from koswat.configuration.settings.koswat_general_settings import SurtaxFactorEnum


def _valid_float_prop(config_property: float) -> bool:
    return config_property is not None and not math.isnan(config_property)


@dataclass
class SurtaxCostsSettings(KoswatConfigProtocol):
    soil_easy: float = math.nan
    soil_normal: float = math.nan
    soil_hard: float = math.nan
    construction_easy: float = math.nan
    construction_normal: float = math.nan
    construction_hard: float = math.nan
    roads_easy: float = math.nan
    roads_normal: float = math.nan
    roads_hard: float = math.nan
    land_purchase_easy: float = math.nan
    land_purchase_normal: float = math.nan
    land_purchase_hard: float = math.nan

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

    def is_valid(self) -> bool:
        return all(_valid_float_prop(_prop) for _prop in self.__dict__.values())
