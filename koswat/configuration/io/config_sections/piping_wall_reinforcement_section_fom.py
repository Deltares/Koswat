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

from typing import Any, Optional

from koswat.configuration.io.config_sections.config_section_fom_protocol import (
    ConfigSectionFomProtocol,
)
from koswat.configuration.io.config_sections.config_section_helper import (
    SectionConfigHelper,
)
from koswat.configuration.settings.koswat_general_settings import SurtaxFactorEnum
from koswat.configuration.settings.reinforcements.koswat_piping_wall_settings import (
    KoswatPipingWallSettings,
)


class PipingWallReinforcementSectionFom(
    ConfigSectionFomProtocol, KoswatPipingWallSettings
):
    @classmethod
    def from_config(
        cls, input_dict: dict[str, Any], set_defaults: bool
    ) -> "PipingWallReinforcementSectionFom":
        _section = cls()

        _active = input_dict.get("actief", None)
        if set_defaults:
            _section.active = SectionConfigHelper.get_bool(_active)
        else:
            _section.active = SectionConfigHelper.get_bool_without_default(_active)

        def _get_enum(input_val: Optional[str]) -> SurtaxFactorEnum:
            if set_defaults:
                return SectionConfigHelper.get_enum(input_val)
            return SectionConfigHelper.get_enum_without_default(input_val)

        _section.soil_surtax_factor = _get_enum(
            input_dict.get("opslagfactor_grond", None)
        )
        _section.constructive_surtax_factor = _get_enum(
            input_dict.get("opslagfactor_constructief", None)
        )
        _section.land_purchase_surtax_factor = _get_enum(
            input_dict.get("opslagfactor_grondaankoop", None)
        )

        def _get_float(input_val: Optional[str]) -> float:
            if set_defaults:
                return SectionConfigHelper.get_float(input_val)
            return SectionConfigHelper.get_float_without_default(input_val)

        _section.min_length_piping_wall = _get_float(
            input_dict.get("min_lengte_kwelscherm", None)
        )
        _section.transition_cbwall_sheetpile = _get_float(
            input_dict.get("overgang_cbwand_damwand", None)
        )
        _section.max_length_piping_wall = _get_float(
            input_dict.get("max_lengte_kwelscherm", None)
        )

        return _section
