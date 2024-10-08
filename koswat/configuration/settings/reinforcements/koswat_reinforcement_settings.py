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
from koswat.configuration.settings.reinforcements.koswat_vps_settings import (
    KoswatVPSSettings,
)


@dataclass
class KoswatReinforcementSettings(KoswatConfigProtocol):
    """
    Wrapper of all settings per reinforcement.
    """

    soil_settings: KoswatSoilSettings = field(default_factory=KoswatSoilSettings)
    vps_settings: KoswatVPSSettings = field(default_factory=KoswatVPSSettings)
    piping_wall_settings: KoswatPipingWallSettings = field(
        default_factory=KoswatPipingWallSettings
    )
    stability_wall_settings: KoswatStabilityWallSettings = field(
        default_factory=KoswatStabilityWallSettings
    )
    cofferdam_settings: KoswatCofferdamSettings = field(
        default_factory=KoswatCofferdamSettings
    )

    def is_valid(self) -> bool:
        return True
