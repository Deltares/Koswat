"""
                GNU GENERAL PUBLIC LICENSE
                  Version 3, 29 June 2007

KOSWAT, from the dutch combination of words `Kosts-Wat` (what are the costs)
Copyright (C) 2025 Stichting Deltares

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

import math

from koswat.dike.koswat_profile_protocol import KoswatProfileProtocol
from koswat.dike_reinforcements.input_profile.soil_waterside.soil_waterside_input_profile import (
    SoilWatersideInputProfile,
)
from koswat.dike_reinforcements.reinforcement_layers.reinforcement_layers_wrapper import (
    ReinforcementLayersWrapper,
)
from koswat.dike_reinforcements.reinforcement_profile.reinforcement_room_calculator import (
    WatersideOnlyRoomCalculator,
)
from koswat.dike_reinforcements.reinforcement_profile.standard.standard_reinforcement_profile import (
    StandardReinforcementProfile,
)


class SoilWatersideReinforcementProfile(StandardReinforcementProfile):
    output_name: str = "Grondmaatregel buitendijks"
    input_data: SoilWatersideInputProfile
    layers_wrapper: ReinforcementLayersWrapper
    old_profile: KoswatProfileProtocol
    new_ground_level_surface: float

    @property
    def waterside_changed(self) -> bool:
        return (
            not math.isclose(
                self.input_data.waterside_slope,
                self.old_profile.input_data.waterside_slope,
            )
            or not math.isclose(
                self.input_data.waterside_berm_width,
                self.old_profile.input_data.waterside_berm_width,
            )
            or not math.isclose(
                self.input_data.waterside_berm_height,
                self.old_profile.input_data.waterside_berm_height,
            )
        )

    def get_reinforcement_room_calculator(self) -> WatersideOnlyRoomCalculator:
        return WatersideOnlyRoomCalculator(
            required_waterside_width=self.waterside_width
        )
