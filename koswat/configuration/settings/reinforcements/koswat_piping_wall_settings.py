from dataclasses import dataclass

from koswat.configuration.koswat_config_protocol import KoswatConfigProtocol
from koswat.configuration.settings.koswat_general_settings import SurtaxFactorEnum


@dataclass
class KoswatPipingWallSettings(KoswatConfigProtocol):
    """
    Settings related to Piping wall reinforcement
    """

    soil_surtax_factor: SurtaxFactorEnum = SurtaxFactorEnum.NORMAAL
    constructive_surtax_factor: SurtaxFactorEnum = SurtaxFactorEnum.NORMAAL
    land_purchase_surtax_factor: SurtaxFactorEnum = SurtaxFactorEnum.NORMAAL
    min_length_piping_wall: float = 0
    transition_cbwall_sheetpile: float = 99
    max_length_piping_wall: float = 99

    def is_valid(self) -> bool:
        return True
