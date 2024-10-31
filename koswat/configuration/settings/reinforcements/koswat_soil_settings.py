from dataclasses import dataclass

from koswat.configuration.koswat_config_protocol import KoswatConfigProtocol
from koswat.configuration.settings.koswat_general_settings import SurtaxFactorEnum


@dataclass
class KoswatSoilSettings(KoswatConfigProtocol):
    """
    Settings related to Soil reinforcement
    """

    soil_surtax_factor: SurtaxFactorEnum = SurtaxFactorEnum.NORMAAL
    land_purchase_surtax_factor: SurtaxFactorEnum = SurtaxFactorEnum.NORMAAL
    min_berm_height: float = 0
    max_berm_height_factor: float = 0
    factor_increase_berm_height: float = 0

    def is_valid(self) -> bool:
        return True
