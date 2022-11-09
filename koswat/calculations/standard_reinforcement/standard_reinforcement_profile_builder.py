from typing import Type

from koswat.builder_protocol import BuilderProtocol
from koswat.calculations.standard_reinforcement.standard_reinforcement_profile_protocol import StandardReinforcementProfile
from koswat.dike.profile.koswat_profile import KoswatProfileBase
from koswat.koswat_scenario import KoswatScenario


class StandardReinforcementProfileBuilder(BuilderProtocol):
    base_profile: KoswatProfileBase
    scenario: KoswatScenario
    reinforcement_profile_type: Type[StandardReinforcementProfile]
