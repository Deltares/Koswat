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

from koswat.configuration.settings.koswat_scenario import KoswatScenario
from koswat.dike.koswat_input_profile_protocol import KoswatInputProfileProtocol
from koswat.dike_reinforcements.reinforcement_profile.berm_calculator.berm_calculator_protocol import (
    BermCalculatorProtocol,
)
from koswat.dike_reinforcements.reinforcement_profile.berm_calculator.berm_calculator_result import (
    BermCalculatorResult,
)


@dataclass
class KeepBermCalculator(BermCalculatorProtocol):
    """
    Calculator for keeping the berm width for the polderside of the dike
    but calculating the height and slope.
    """

    scenario: KoswatScenario
    dikebase_piping_old: float
    dikebase_piping_new: float
    dike_height_new: float

    def calculate(
        self,
        base_data: KoswatInputProfileProtocol,
        reinforced_data: KoswatInputProfileProtocol,
    ) -> BermCalculatorResult:
        _polderside_berm_width = (
            base_data.polderside_berm_width
        )  # maintain current berm polderside
        _polderside_berm_height = self._calculate_new_keep_polderside_berm_height(
            base_data
        )
        _polderside_slope = self._calculate_new_keep_polderside_slope(base_data)

        return BermCalculatorResult(
            berm_width=_polderside_berm_width,
            berm_height=_polderside_berm_height,
            slope=_polderside_slope,
        )

    def _calculate_new_keep_polderside_berm_height(
        self, base_data: KoswatInputProfileProtocol
    ) -> float:
        _dike_height_old = base_data.crest_height - base_data.polderside_ground_level
        _berm_height_old = (
            base_data.polderside_berm_height - base_data.polderside_ground_level
        )
        _berm_factor_old = _berm_height_old / _dike_height_old

        return base_data.polderside_berm_height + _berm_factor_old * self.scenario.d_h

    def _calculate_new_keep_polderside_slope(
        self, base_data: KoswatInputProfileProtocol
    ) -> float:
        _operand = (
            base_data.crest_height - base_data.polderside_ground_level
        ) * base_data.polderside_slope
        _dividend = (
            base_data.crest_height
            - base_data.polderside_ground_level
            + self.scenario.d_h
        )
        return _operand / _dividend
