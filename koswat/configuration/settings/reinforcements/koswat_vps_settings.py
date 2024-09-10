from dataclasses import dataclass

from koswat.configuration.koswat_config_protocol import KoswatConfigProtocol
from koswat.configuration.settings.koswat_general_settings import SurtaxFactorEnum


@dataclass
class KoswatVPSSettings(KoswatConfigProtocol):
    """
    Settings related to Vertical Piping Solution reinforcement
    """

    soil_surtax_factor: SurtaxFactorEnum = SurtaxFactorEnum.NORMAAL
    construction_surtax_factor: SurtaxFactorEnum = SurtaxFactorEnum.NORMAAL
    land_purchase_surtax_factor: SurtaxFactorEnum = SurtaxFactorEnum.NORMAAL
    binnen_berm_breedte_vps: float = 0

    def is_valid(self) -> bool:
        return True
