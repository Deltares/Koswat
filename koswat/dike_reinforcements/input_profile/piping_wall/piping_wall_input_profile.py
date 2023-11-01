import math
from dataclasses import dataclass

from koswat.configuration.settings.koswat_general_settings import ConstructionTypeEnum
from koswat.dike.profile.koswat_input_profile_base import KoswatInputProfileBase
from koswat.dike_reinforcements.input_profile.reinforcement_input_profile_protocol import (
    ReinforcementInputProfileProtocol,
)


@dataclass
class PipingWallInputProfile(KoswatInputProfileBase, ReinforcementInputProfileProtocol):
    construction_length: float = math.nan
    construction_type: ConstructionTypeEnum | None = None

    @property
    def reinforcement_domain_name(self) -> str:
        return "Kwelscherm"
