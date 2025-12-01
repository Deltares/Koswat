"""
                    GNU GENERAL PUBLIC LICENSE
                      Version 3, 29 June 2007

    KOSWAT, from the dutch combination of words `Kosts-Wat` (what are the costs)
    Copyright (C) 2024 Stichting Deltares

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program.  If not, see <http://www.gnu.org/licenses/>.
"""

from typing import Protocol, runtime_checkable

from koswat.configuration.settings import KoswatScenario
from koswat.configuration.settings.reinforcements.koswat_reinforcement_settings import (
    KoswatReinforcementSettings,
)
from koswat.core.protocols import BuilderProtocol
from koswat.dike.profile.koswat_profile import KoswatProfileBase
from koswat.dike_reinforcements.reinforcement_profile.reinforcement_profile_protocol import (
    ReinforcementProfileProtocol,
)


@runtime_checkable
class ReinforcementProfileBuilderProtocol(BuilderProtocol, Protocol):
    base_profile: KoswatProfileBase
    reinforcement_settings: KoswatReinforcementSettings
    scenario: KoswatScenario
    reinforcement_profile_type: type[ReinforcementProfileProtocol]

    def build(self) -> ReinforcementProfileProtocol:
        """
        Builds a concrete instance of a `ReinforcementProfileProtocol` based on the required data.

        Returns:
            ReinforcementProfileProtocol: Valid instance of a `ReinforcementProfileProtocol`.
        """
        pass
