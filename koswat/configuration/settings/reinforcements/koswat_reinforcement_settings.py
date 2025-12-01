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
