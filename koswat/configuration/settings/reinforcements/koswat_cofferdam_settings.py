from dataclasses import dataclass

from koswat.configuration.koswat_config_protocol import KoswatConfigProtocol
from koswat.configuration.settings.koswat_general_settings import SurtaxFactorEnum


@dataclass
class KoswatCofferdamSettings(KoswatConfigProtocol):
    """
    Settings related to Cofferdam reinforcement
    """

    soil_surtax_factor: SurtaxFactorEnum = SurtaxFactorEnum.NORMAAL
    constructive_surtax_factor: SurtaxFactorEnum = SurtaxFactorEnum.NORMAAL
    min_length_cofferdam: float = 0
    max_length_cofferdam: float = 99

    def is_valid(self) -> bool:
        return True
