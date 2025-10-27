from dataclasses import dataclass

from koswat.configuration.koswat_config_protocol import KoswatConfigProtocol
from koswat.configuration.settings.koswat_general_settings import SurtaxFactorEnum


@dataclass
class KoswatStabilityWallSettings(KoswatConfigProtocol):
    """
    Settings related to Stability wall reinforcement
    """

    active: bool = True
    soil_surtax_factor: SurtaxFactorEnum = SurtaxFactorEnum.NORMAAL
    constructive_surtax_factor: SurtaxFactorEnum = SurtaxFactorEnum.NORMAAL
    land_purchase_surtax_factor: SurtaxFactorEnum = SurtaxFactorEnum.NORMAAL
    steepening_polderside_slope: float = 0
    min_length_stability_wall: float = 0
    transition_sheetpile_diaphragm_wall: float = 99
    max_length_stability_wall: float = 99

    def is_valid(self) -> bool:
        return True
