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

from dataclasses import dataclass, field
from typing import Any, Optional

from koswat.configuration.io.config_sections.config_section_helper import (
    SectionConfigHelper,
)
from koswat.core.io.json.koswat_json_fom_protocol import KoswatJsonFomProtocol


@dataclass
class SurroundingsSectionFom(KoswatJsonFomProtocol):
    construction_distance: float
    construction_buffer: float
    waterside: bool
    allow_waterside_reinforcement: bool
    obstacle_types: dict[str, Optional[float]] = field(default_factory=dict)

    @classmethod
    def from_config(cls, input_config: dict[str, Any], set_defaults: bool = True) -> "SurroundingsSectionFom":
        def _get_float(input_val: Optional[str]) -> float:
            if set_defaults:
                return SectionConfigHelper.get_float(input_val)
            return SectionConfigHelper.get_float_without_default(input_val)
        def _get_bool(input_val: Optional[str], default_value: bool) -> bool:
            if set_defaults:
                return SectionConfigHelper.get_bool(input_val, default_value)
            return SectionConfigHelper.get_bool_without_default(input_val)

        _section = cls(
            construction_distance=_get_float(
                input_config.get("constructieafstand", None)
            ),
            construction_buffer=_get_float(
                input_config.get("constructieovergang", None)
            ),
            waterside=_get_bool(input_config.get("buitendijks", None), False),
            allow_waterside_reinforcement=_get_bool(
                input_config.get("toegestaanbuitenzijdeversterking", None),
                True
            ),
            obstacle_types={
                _type.get("type").lower().strip(): _get_float(_type.get("buffer", None))
                for _type in input_config.get("omgevingtypes", [])
            },
        )
        return _section
