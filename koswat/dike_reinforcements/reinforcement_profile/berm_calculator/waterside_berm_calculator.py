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

from dataclasses import dataclass

from koswat.configuration.settings.reinforcements.koswat_reinforcement_settings import (
    KoswatReinforcementSettings,
)
from koswat.dike.koswat_input_profile_protocol import KoswatInputProfileProtocol
from koswat.dike_reinforcements.reinforcement_profile.berm_calculator.berm_calculator_protocol import (
    BermCalculatorProtocol,
)
from koswat.dike_reinforcements.reinforcement_profile.berm_calculator.berm_calculator_result import (
    BermCalculatorResult,
)


@dataclass
class WatersideBermCalculator(BermCalculatorProtocol):
    """
    Calculator for the berm width, height and slope for the waterside of the dike.
    """

    reinforcement_settings: KoswatReinforcementSettings
    dikebase_piping_old: float
    dikebase_piping_new: float
    dike_height_new: float
    d_p: float

    def calculate(
        self,
        base_data: KoswatInputProfileProtocol,
        reinforced_data: KoswatInputProfileProtocol,
    ) -> BermCalculatorResult:
        _dikebase_piping_needed = self.dikebase_piping_old + self.d_p
        _seepage_length = max(_dikebase_piping_needed - self.dikebase_piping_new, 0)
        _waterside_berm_width = reinforced_data.waterside_berm_width + _seepage_length

        return BermCalculatorResult(
            berm_width=_waterside_berm_width,
            berm_height=self._calculate_new_waterside_berm_height_piping(
                reinforced_data
            ),
            slope=reinforced_data.waterside_slope,
        )

    def _calculate_new_waterside_berm_height_piping(
        self,
        reinforced_data: KoswatInputProfileProtocol,
    ) -> float:
        _old_berm_height = 0.0
        _max = max(
            self.reinforcement_settings.soil_settings.min_berm_height,
            _old_berm_height,
            reinforced_data.waterside_berm_width
            * self.reinforcement_settings.soil_waterside_settings.factor_increase_berm_height,
        )
        return (
            min(
                _max,
                self.reinforcement_settings.soil_waterside_settings.max_berm_height_factor
                * (
                    reinforced_data.crest_height
                    - reinforced_data.waterside_ground_level
                ),
            )
            + reinforced_data.waterside_ground_level
        )
