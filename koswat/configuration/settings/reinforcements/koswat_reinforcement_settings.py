from dataclasses import dataclass

from koswat.configuration.koswat_config_protocol import KoswatConfigProtocol
from koswat.configuration.settings.reinforcements.koswat_piping_settings import (
    KoswatPipingSettings,
)


@dataclass
class KoswatReinforcementSettings(KoswatConfigProtocol):
    """
    Wrapper of all settings per reinforcement.
    """

    piping_settings: KoswatPipingSettings

    def is_valid(self) -> bool:
        return True
