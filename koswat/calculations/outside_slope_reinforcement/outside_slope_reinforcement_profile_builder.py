from typing import Type

from koswat.builder_protocol import BuilderProtocol
from koswat.calculations.outside_slope_reinforcement.outside_slope_reinforcement_profile_protocol import (
    OutsideSlopeReinforcementProfile,
)
from koswat.dike.profile.koswat_profile import KoswatProfileBase
from koswat.koswat_scenario import KoswatScenario


class OutsideSlopeReinforcementProfileBuilder(BuilderProtocol):
    base_profile: KoswatProfileBase
    scenario: KoswatScenario
    reinforcement_profile_type: Type[OutsideSlopeReinforcementProfile]
