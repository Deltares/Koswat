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
from dataclasses import dataclass

from koswat.configuration.koswat_config_protocol import KoswatConfigProtocol
from koswat.configuration.settings.koswat_general_settings import SurtaxFactorEnum


def _valid_float_prop(config_property: float) -> bool:
    return config_property is not None and not math.isnan(config_property)


@dataclass
class SurtaxCostsSettings(KoswatConfigProtocol):
    soil_easy: float = math.nan
    soil_normal: float = math.nan
    soil_hard: float = math.nan
    construction_easy: float = math.nan
    construction_normal: float = math.nan
    construction_hard: float = math.nan
    roads_easy: float = math.nan
    roads_normal: float = math.nan
    roads_hard: float = math.nan
    land_purchase_easy: float = math.nan
    land_purchase_normal: float = math.nan
    land_purchase_hard: float = math.nan

    def _get_surtax(
        self, surtax_type: str, surtax_factor: SurtaxFactorEnum | None
    ) -> float:
        if not surtax_factor:
            return 0
        if surtax_factor == SurtaxFactorEnum.MAKKELIJK:
            level = "easy"
        elif surtax_factor == SurtaxFactorEnum.NORMAAL:
            level = "normal"
        elif surtax_factor == SurtaxFactorEnum.MOEILIJK:
            level = "hard"
        return getattr(self, f"{surtax_type}_{level}")

    def get_soil_surtax(
        self,
        surtax_factor: SurtaxFactorEnum,
    ) -> float:
        return self._get_surtax("soil", surtax_factor)

    def get_constructive_surtax(
        self,
        surtax_factor: SurtaxFactorEnum | None,
    ) -> float:
        return self._get_surtax("construction", surtax_factor)

    def get_land_purchase_surtax(
        self,
        surtax_factor: SurtaxFactorEnum | None,
    ) -> float:
        return self._get_surtax("land_purchase", surtax_factor)

    def is_valid(self) -> bool:
        return all(_valid_float_prop(_prop) for _prop in self.__dict__.values())
