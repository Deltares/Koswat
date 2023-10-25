from dataclasses import dataclass

from koswat.configuration.koswat_config_protocol import KoswatConfigProtocol
from koswat.configuration.settings.koswat_general_settings import SurtaxFactorEnum


@dataclass
class KoswatPipingSettings(KoswatConfigProtocol):
    """
    Settings related to Piping reinforcement
    """

    soil_surtax_factor: SurtaxFactorEnum = SurtaxFactorEnum.NORMAAL
    constructive_surtax_factor: SurtaxFactorEnum = SurtaxFactorEnum.NORMAAL
    land_purchase_surtax_factor: SurtaxFactorEnum = SurtaxFactorEnum.NORMAAL
    min_lengte_kwelscherm: float = 0
    overgang_cbwand_damwand: float = 0
    max_lengte_kwelscherm: float = 0

    def is_valid(self) -> bool:
        return True
