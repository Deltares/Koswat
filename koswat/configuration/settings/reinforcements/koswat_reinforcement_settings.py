from dataclasses import dataclass

from koswat.configuration.koswat_config_protocol import KoswatConfigProtocol
from koswat.configuration.settings.reinforcements.koswat_cofferdam_settings import (
    KoswatCofferdamSettings,
)
from koswat.configuration.settings.reinforcements.koswat_piping_settings import (
    KoswatPipingSettings,
)
from koswat.configuration.settings.reinforcements.koswat_soil_settings import (
    KoswatSoilSettings,
)
from koswat.configuration.settings.reinforcements.koswat_stability_wall_settings import (
    KoswatStabilityWallSettings,
)


@dataclass
class KoswatReinforcementSettings(KoswatConfigProtocol):
    """
    Wrapper of all settings per reinforcement.
    """

    soil_settings: KoswatSoilSettings
    piping_settings: KoswatPipingSettings
    stability_wall_settings: KoswatStabilityWallSettings
    cofferdam_settings: KoswatCofferdamSettings

    def is_valid(self) -> bool:
        return True
