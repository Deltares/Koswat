from dataclasses import dataclass

from koswat.configuration.koswat_config_protocol import KoswatConfigProtocol
from koswat.configuration.settings.koswat_general_settings import SurtaxFactorEnum


@dataclass
class KoswatStabilityWallSettings(KoswatConfigProtocol):
    """
    Settings related to Stability wall reinforcement
    """

    soil_surtax_factor: SurtaxFactorEnum = SurtaxFactorEnum.NORMAAL
    constructive_surtax_factor: SurtaxFactorEnum = SurtaxFactorEnum.NORMAAL
    land_purchase_surtax_factor: SurtaxFactorEnum = SurtaxFactorEnum.NORMAAL
    versteiling_binnentalud: float = 0
    min_lengte_stabiliteitswand: float = 0
    overgang_damwand_diepwand: float = 0
    max_lengte_stabiliteitswand: float = 0

    def is_valid(self) -> bool:
        return True
