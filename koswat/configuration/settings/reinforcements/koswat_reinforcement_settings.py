from dataclasses import dataclass, field

from koswat.configuration.koswat_config_protocol import KoswatConfigProtocol
from koswat.configuration.settings.reinforcements.koswat_cofferdam_settings import (
    KoswatCofferdamSettings,
)
from koswat.configuration.settings.reinforcements.koswat_piping_wall_settings import (
    KoswatPipingWallSettings,
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

    soil_settings: KoswatSoilSettings = field(
        default_factory=lambda: KoswatSoilSettings()
    )
    piping_wall_settings: KoswatPipingWallSettings = field(
        default_factory=lambda: KoswatPipingWallSettings()
    )
    stability_wall_settings: KoswatStabilityWallSettings = field(
        default_factory=lambda: KoswatStabilityWallSettings()
    )
    cofferdam_settings: KoswatCofferdamSettings = field(
        default_factory=lambda: KoswatCofferdamSettings()
    )

    def is_valid(self) -> bool:
        return True
