import math

from koswat.configuration.koswat_config_protocol import KoswatConfigProtocol


class ConstructionFactors:
    c_factor: float
    d_factor: float
    z_factor: float
    f_factor: float
    g_factor: float

    def __init__(self) -> None:
        self.c_factor = math.nan
        self.d_factor = math.nan
        self.z_factor = math.nan
        self.f_factor = math.nan
        self.g_factor = math.nan

    def _isvalid(self) -> bool:
        return (
            not math.isnan(self.c_factor)
            and not math.isnan(self.d_factor)
            and not math.isnan(self.z_factor)
            and not math.isnan(self.f_factor)
            and not math.isnan(self.g_factor)
        )


class ConstructionCostsSettings(KoswatConfigProtocol):
    cb_damwand: ConstructionFactors
    damwand_onverankerd: ConstructionFactors
    damwand_verankerd: ConstructionFactors
    diepwand: ConstructionFactors
    kistdam: ConstructionFactors

    def __init__(self) -> None:
        self.cb_damwand = None
        self.damwand_onverankerd = None
        self.damwand_verankerd = None
        self.diepwand = None
        self.kistdam = None

    def is_valid(self):
        return (
            self.cb_damwand.isvalid()
            and self.damwand_onverankerd.isvalid()
            and self.damwand_verankerd.isvalid()
            and self.diepwand.isvalid()
            and self.kistdam.isvalid()
        )
