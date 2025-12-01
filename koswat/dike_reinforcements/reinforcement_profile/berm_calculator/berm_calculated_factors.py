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

from __future__ import annotations

from collections import defaultdict
from dataclasses import dataclass

from koswat.configuration.settings.koswat_scenario import KoswatScenario
from koswat.configuration.settings.reinforcements.koswat_reinforcement_settings import (
    KoswatReinforcementSettings,
)
from koswat.dike.koswat_input_profile_protocol import KoswatInputProfileProtocol
from koswat.dike_reinforcements.input_profile.input_profile_enum import InputProfileEnum


@dataclass
class BermCalculatedFactors:
    """
    Factors used to create the right calculator.
    """

    reinforcement_settings: KoswatReinforcementSettings
    scenario: KoswatScenario
    dikebase_piping_old: float
    dikebase_piping_new_dict: dict[InputProfileEnum, float]
    dikebase_height_new: float
    dikebase_stability_new: float
    berm_old_is_stability: bool
    berm_factor_old: float
    dike_height_new: float

    def get_dikebase_piping_new(self, reinforcement_type: InputProfileEnum) -> float:
        """
        Get the right dikebase piping factor for the given reinforcement type.

        Args:
            reinforcement_type (InputProfileEnum): The reinforcement type.

        Returns:
            float: The dikebase piping factor for the given reinforcement type.
        """
        if reinforcement_type in self.dikebase_piping_new_dict.keys():
            return self.dikebase_piping_new_dict[reinforcement_type]
        return self.dikebase_piping_new_dict[InputProfileEnum.NONE]

    @classmethod
    def from_calculation_input(
        cls,
        base_data: KoswatInputProfileProtocol,
        reinforced_data: KoswatInputProfileProtocol,
        reinforcement_settings: KoswatReinforcementSettings,
        scenario: KoswatScenario,
    ) -> BermCalculatedFactors:
        """
        Create the factors based on the input data.

        Args:
            base_data (KoswatInputProfileProtocol): The input data of the base profile.
            reinforced_data (KoswatInputProfileProtocol): The input data of the reinforced profile.
            reinforcement_settings (KoswatReinforcementSettings): The reinforcement settings.
            scenario (KoswatScenario): The scenario used.

        Returns:
            BermCalculatorFactors: The factors used to create the right calculator.
        """
        _dike_height_old = base_data.crest_height - base_data.polderside_ground_level
        _berm_height_old = (
            base_data.polderside_berm_height - base_data.polderside_ground_level
        )
        _berm_factor_old = _berm_height_old / _dike_height_old
        _berm_old_is_stability = (
            _berm_factor_old
            > reinforcement_settings.soil_settings.max_berm_height_factor
        )

        _dikebase_stability_old = (
            base_data.crest_width
            + _dike_height_old * base_data.polderside_slope
            + _berm_old_is_stability * base_data.polderside_berm_width
        )
        _dikebase_piping_old = (
            base_data.crest_width
            + _dike_height_old * base_data.polderside_slope
            + base_data.polderside_berm_width
        )

        _dike_height_new = (
            base_data.crest_height + scenario.d_h - base_data.polderside_ground_level
        )
        _dikebase_height_new = (
            scenario.d_h * reinforced_data.waterside_slope
            + base_data.crest_width
            + _dike_height_new * base_data.polderside_slope
        )
        _dikebase_stability_new = _dikebase_stability_old + scenario.d_s

        _dikebase_piping_new_dict = defaultdict(float)
        _dikebase_piping_new_dict[InputProfileEnum.NONE] = (
            _dikebase_piping_old + scenario.d_p
        )
        _dikebase_piping_new_dict[InputProfileEnum.PIPING_WALL] = max(
            _dikebase_piping_old,
            _dikebase_height_new,
            _dikebase_stability_new,
        )
        _dikebase_piping_new_dict[InputProfileEnum.VPS] = max(
            _dikebase_piping_old,
            max(_dikebase_height_new, _dikebase_stability_new)
            + reinforcement_settings.vps_settings.polderside_berm_width_vps,
        )

        return cls(
            reinforcement_settings=reinforcement_settings,
            scenario=scenario,
            dikebase_piping_old=_dikebase_piping_old,
            dikebase_piping_new_dict=_dikebase_piping_new_dict,
            dikebase_height_new=_dikebase_height_new,
            dikebase_stability_new=_dikebase_stability_new,
            berm_old_is_stability=_berm_old_is_stability,
            berm_factor_old=_berm_factor_old,
            dike_height_new=_dike_height_new,
        )
