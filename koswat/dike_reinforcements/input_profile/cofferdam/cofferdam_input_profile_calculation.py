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

from dataclasses import asdict

from koswat.configuration.settings import KoswatScenario
from koswat.configuration.settings.koswat_general_settings import ConstructionTypeEnum
from koswat.configuration.settings.reinforcements.koswat_cofferdam_settings import (
    KoswatCofferdamSettings,
)
from koswat.configuration.settings.reinforcements.koswat_reinforcement_settings import (
    KoswatReinforcementSettings,
)
from koswat.dike.koswat_input_profile_protocol import KoswatInputProfileProtocol
from koswat.dike.koswat_profile_protocol import KoswatProfileProtocol
from koswat.dike_reinforcements.input_profile.cofferdam.cofferdam_input_profile import (
    CofferDamInputProfile,
)
from koswat.dike_reinforcements.input_profile.input_profile_enum import InputProfileEnum
from koswat.dike_reinforcements.input_profile.reinforcement_input_profile_calculation_base import (
    ReinforcementInputProfileCalculationBase,
)
from koswat.dike_reinforcements.input_profile.reinforcement_input_profile_calculation_protocol import (
    ReinforcementInputProfileCalculationProtocol,
)
from koswat.dike_reinforcements.reinforcement_profile.berm_calculator.berm_calculated_factors import (
    BermCalculatedFactors,
)
from koswat.dike_reinforcements.reinforcement_profile.berm_calculator.berm_calculator_factory import (
    BermCalculatorFactory,
)


class CofferdamInputProfileCalculation(
    ReinforcementInputProfileCalculationBase,
    ReinforcementInputProfileCalculationProtocol,
):
    base_profile: KoswatProfileProtocol
    reinforcement_settings: KoswatReinforcementSettings
    scenario: KoswatScenario

    def __init__(self) -> None:
        self.base_profile = None
        self.scenario = None

    @staticmethod
    def _calculate_length_cofferdam(
        old_data: KoswatInputProfileProtocol,
        cofferdam_settings: KoswatCofferdamSettings,
        seepage_length: float,
        new_crest_height: float,
    ) -> float:
        _length_stability = (new_crest_height - 0.5) - (old_data.pleistocene - 1.0)
        if seepage_length == 0.0:
            # Length of wall is not determined by piping.
            _length_piping = 0.0
        else:
            _length_piping = (
                (seepage_length / 6.0) + (new_crest_height - 0.5) - old_data.aquifer
            )

        return round(
            min(
                max(
                    _length_piping,
                    _length_stability,
                    cofferdam_settings.min_length_cofferdam,
                ),
                cofferdam_settings.max_length_cofferdam,
            ),
            1,
        )

    @staticmethod
    def _determine_construction_type(
        construction_length: float,
    ) -> ConstructionTypeEnum | None:
        if construction_length == 0.0:
            return None
        else:
            return ConstructionTypeEnum.KISTDAM

    @staticmethod
    def _calculate_new_waterside_slope(
        base_data: KoswatInputProfileProtocol, scenario: KoswatScenario
    ) -> float:
        _operand = (
            base_data.crest_height - base_data.waterside_ground_level
        ) * base_data.waterside_slope
        _dividend = (
            base_data.crest_height - base_data.waterside_ground_level + scenario.d_h
        )
        return _operand / _dividend

    def build(self) -> CofferDamInputProfile:
        _reinforced_data = self._get_reinforcement_profile(
            CofferDamInputProfile, self.base_profile.input_data, self.scenario
        )
        assert isinstance(_reinforced_data, CofferDamInputProfile)

        _reinforced_data.active = self.reinforcement_settings.cofferdam_settings.active

        # Berm calculation
        _calculated_factors = BermCalculatedFactors.from_calculation_input(
            self.base_profile.input_data,
            _reinforced_data,
            self.reinforcement_settings,
            self.scenario,
        )
        _polderside_berm_calculator = BermCalculatorFactory.get_berm_calculator(
            InputProfileEnum.COFFERDAM, _calculated_factors
        )
        (
            _reinforced_data.polderside_berm_width,
            _reinforced_data.polderside_berm_height,
            _reinforced_data.polderside_slope,
        ) = asdict(
            _polderside_berm_calculator.calculate(
                self.base_profile.input_data, _reinforced_data
            )
        ).values()

        # Construction calculations
        _seepage_length = self.scenario.d_p
        _reinforced_data.construction_length = self._calculate_length_cofferdam(
            self.base_profile.input_data,
            self.reinforcement_settings.cofferdam_settings,
            _seepage_length,
            _reinforced_data.crest_height,
        )
        _reinforced_data.construction_type = self._determine_construction_type(
            _reinforced_data.construction_length
        )

        # Settings
        _reinforced_data.soil_surtax_factor = (
            self.reinforcement_settings.cofferdam_settings.soil_surtax_factor
        )
        _reinforced_data.constructive_surtax_factor = (
            self.reinforcement_settings.cofferdam_settings.constructive_surtax_factor
        )
        _reinforced_data.land_purchase_surtax_factor = None

        return _reinforced_data
