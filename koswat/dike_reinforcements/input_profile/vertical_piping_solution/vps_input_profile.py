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

from koswat.configuration.settings.koswat_general_settings import (
    ConstructionTypeEnum,
    SurtaxFactorEnum,
)
from koswat.dike.profile.koswat_input_profile_base import KoswatInputProfileBase
from koswat.dike_reinforcements.input_profile.reinforcement_input_profile_protocol import (
    ReinforcementInputProfileProtocol,
)


@dataclass
class VPSInputProfile(KoswatInputProfileBase, ReinforcementInputProfileProtocol):
    active: bool = True
    construction_length: float = 0.0
    construction_type: ConstructionTypeEnum | None = None
    soil_surtax_factor: SurtaxFactorEnum = SurtaxFactorEnum.NORMAAL
    constructive_surtax_factor: SurtaxFactorEnum | None = None
    land_purchase_surtax_factor: SurtaxFactorEnum | None = None

    @property
    def reinforcement_domain_name(self) -> str:
        return "Verticale piping oplossing"

    @property
    def ground_price(self) -> float:
        return self.ground_price_unbuilt
