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

from koswat.configuration.io.config_sections.config_section_helper import (
    SectionConfigHelper,
)
from koswat.configuration.io.config_sections.stability_wall_toe_reinforcement_section_fom import (
    StabilityWallToeReinforcementSectionFom,
)


class StabilityWallCrestReinforcementSectionFom(
    StabilityWallToeReinforcementSectionFom
):
    @classmethod
    def from_config(
        cls, input_dict: dict[str, Any], set_defaults: bool
    ) -> "StabilityWallCrestReinforcementSectionFom":
        _section = super().from_config(input_dict, set_defaults)

        def _get_float(input_val: Optional[str]) -> float:
            if set_defaults:
                return SectionConfigHelper.get_float(input_val)
            return SectionConfigHelper.get_float_without_default(input_val)

        _section.transition_sheetpile_diaphragm_wall = _get_float(
            input_dict.get("overgang_damwand_diepwand", None)
        )

        return _section
