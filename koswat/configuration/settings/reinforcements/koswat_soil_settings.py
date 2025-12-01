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
from typing import Any

from koswat.configuration.koswat_config_protocol import KoswatConfigProtocol
from koswat.configuration.settings.koswat_general_settings import SurtaxFactorEnum


@dataclass
class KoswatSoilSettings(KoswatConfigProtocol):
    """
    Settings related to Soil reinforcement
    """

    active: bool = True
    soil_surtax_factor: SurtaxFactorEnum = SurtaxFactorEnum.NORMAAL
    land_purchase_surtax_factor: SurtaxFactorEnum = SurtaxFactorEnum.NORMAAL
    min_berm_height: float = 0.5
    max_berm_height_factor: float = 0.4
    factor_increase_berm_height: float = 0.05

    def is_valid(self) -> bool:
        return True

    def set_defaults(self, other: "KoswatSoilSettings") -> "KoswatSoilSettings":
        """
        Add the defaults from another KoswatSoilSettings instance to this instance, if not set.

        Args:
            other (KoswatSoilSettings): The other instance to get defaults from.

        Raises:
            TypeError: If the other instance has a different type.

        Returns:
            KoswatSoilSettings: The instance with defaults set.
        """
        if not isinstance(other, KoswatSoilSettings):
            raise TypeError("Can only merge with another KoswatSoilSettings instance.")

        def _set_default(this_value: Any, other_value: Any) -> Any:
            if this_value is None:
                return other_value
            return this_value

        self.active = _set_default(self.active, other.active)
        self.soil_surtax_factor = _set_default(
            self.soil_surtax_factor, other.soil_surtax_factor
        )
        self.land_purchase_surtax_factor = _set_default(
            self.land_purchase_surtax_factor, other.land_purchase_surtax_factor
        )
        self.min_berm_height = _set_default(self.min_berm_height, other.min_berm_height)
        self.max_berm_height_factor = _set_default(
            self.max_berm_height_factor, other.max_berm_height_factor
        )
        self.factor_increase_berm_height = _set_default(
            self.factor_increase_berm_height, other.factor_increase_berm_height
        )

        return self
