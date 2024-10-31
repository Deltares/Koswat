import logging
import math
from dataclasses import dataclass

from koswat.configuration.koswat_config_protocol import KoswatConfigProtocol
from koswat.configuration.settings.koswat_general_settings import ConstructionTypeEnum


@dataclass
class ConstructionFactors:
    c_factor: float = math.nan
    d_factor: float = math.nan
    z_factor: float = math.nan
    f_factor: float = math.nan
    g_factor: float = math.nan

    def is_valid(self) -> bool:
        return (
            not math.isnan(self.c_factor)
            and not math.isnan(self.d_factor)
            and not math.isnan(self.z_factor)
            and not math.isnan(self.f_factor)
            and not math.isnan(self.g_factor)
        )


@dataclass
class ConstructionCostsSettings(KoswatConfigProtocol):
    vzg: ConstructionFactors | None = None
    cb_sheetpile: ConstructionFactors | None = None
    sheetpile_unanchored: ConstructionFactors | None = None
    sheetpile_anchored: ConstructionFactors | None = None
    diaphragm_wall: ConstructionFactors | None = None
    cofferdam: ConstructionFactors | None = None

    def get_construction_factors(
        self, construction_type: ConstructionTypeEnum | None
    ) -> ConstructionFactors | None:
        if not construction_type:
            return None
        if construction_type == ConstructionTypeEnum.VZG:
            return self.vzg
        if construction_type == ConstructionTypeEnum.CB_DAMWAND:
            return self.cb_sheetpile
        if construction_type == ConstructionTypeEnum.DAMWAND_ONVERANKERD:
            return self.sheetpile_unanchored
        if construction_type == ConstructionTypeEnum.DAMWAND_VERANKERD:
            return self.sheetpile_anchored
        if construction_type == ConstructionTypeEnum.DIEPWAND:
            return self.diaphragm_wall
        if construction_type == ConstructionTypeEnum.KISTDAM:
            return self.cofferdam
        logging.warning("Unsupported construction type {}".format(construction_type))

    def is_valid(self):
        return (
            self.vzg.is_valid()
            and self.cb_sheetpile.is_valid()
            and self.sheetpile_unanchored.is_valid()
            and self.sheetpile_anchored.is_valid()
            and self.diaphragm_wall.is_valid()
            and self.cofferdam.is_valid()
        )
