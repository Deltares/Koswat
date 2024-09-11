from dataclasses import dataclass

from koswat.dike_reinforcements.input_profile.reinforcement_input_profile_protocol import (
    ReinforcementInputProfileProtocol,
)
from koswat.dike_reinforcements.input_profile.soil.soil_input_profile import (
    SoilInputProfile,
)


@dataclass
class VPSInputProfile(SoilInputProfile, ReinforcementInputProfileProtocol):
    @property
    def reinforcement_domain_name(self) -> str:
        return "Verticale piping oplossing"

    @property
    def grondprijs(self) -> float:
        return self.grondprijs_bebouwd
