from typing import Protocol, runtime_checkable

from koswat.configuration.settings import KoswatScenario
from koswat.configuration.settings.reinforcements.koswat_reinforcement_settings import (
    KoswatReinforcementSettings,
)
from koswat.core.protocols import BuilderProtocol
from koswat.dike.koswat_profile_protocol import KoswatProfileProtocol
from koswat.dike_reinforcements.input_profile.reinforcement_input_profile_protocol import (
    ReinforcementInputProfileProtocol,
)


@runtime_checkable
class ReinforcementInputProfileCalculationProtocol(BuilderProtocol, Protocol):
    base_profile: KoswatProfileProtocol
    reinforcement_settings: KoswatReinforcementSettings
    scenario: KoswatScenario

    def build(self) -> ReinforcementInputProfileProtocol:
        """
        Builds a `ReinforcementInputProfileProtocol` instance based on the `base_profile` and `scenario` specified in this class.

        Returns:
            ReinforcementInputProfileProtocol: Calculated reinforcement input profile.
        """
        pass
