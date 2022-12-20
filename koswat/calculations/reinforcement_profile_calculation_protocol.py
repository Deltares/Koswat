from typing import Protocol, runtime_checkable

from koswat.builder_protocol import BuilderProtocol
from koswat.calculations.reinforcement_input_profile_protocol import (
    ReinforcementInputProfileProtocol,
)
from koswat.configuration.settings import KoswatScenario
from koswat.dike.koswat_profile_protocol import KoswatProfileProtocol


@runtime_checkable
class ReinforcementInputProfileCalculationProtocol(BuilderProtocol, Protocol):
    base_profile: KoswatProfileProtocol
    scenario: KoswatScenario

    def build(self) -> ReinforcementInputProfileProtocol:
        """
        Builds a `ReinforcementInputProfileProtocol` instance based on the `base_profile` and `scenario` specified in this class.

        Returns:
            ReinforcementInputProfileProtocol: Calculated reinforcement input profile.
        """
        pass
