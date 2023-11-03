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
    cb_damwand: ConstructionFactors | None = None
    damwand_onverankerd: ConstructionFactors | None = None
    damwand_verankerd: ConstructionFactors | None = None
    diepwand: ConstructionFactors | None = None
    kistdam: ConstructionFactors | None = None

    def get_construction_factors(
        self, construction_type: ConstructionTypeEnum | None
    ) -> ConstructionFactors | None:
        if not construction_type:
            return None
        if construction_type == ConstructionTypeEnum.CB_DAMWAND:
            return self.cb_damwand
        elif construction_type == ConstructionTypeEnum.DAMWAND_ONVERANKERD:
            return self.damwand_onverankerd
        elif construction_type == ConstructionTypeEnum.DAMWAND_VERANKERD:
            return self.damwand_verankerd
        elif construction_type == ConstructionTypeEnum.DIEPWAND:
            return self.diepwand
        elif construction_type == ConstructionTypeEnum.KISTDAM:
            return self.kistdam
        else:
            logging.warning(
                "Unsupported construction type {}".format(construction_type)
            )

    def is_valid(self):
        return (
            self.cb_damwand.is_valid()
            and self.damwand_onverankerd.is_valid()
            and self.damwand_verankerd.is_valid()
            and self.diepwand.is_valid()
            and self.kistdam.is_valid()
        )
