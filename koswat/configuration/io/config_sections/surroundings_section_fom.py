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
    construction_distance: float = float("nan")
    construction_buffer: float = float("nan")
    waterside: bool = False
    allow_waterside_reinforcement: bool = True
    obstacle_types: dict[str, Optional[float]] = field(default_factory=dict)

    @classmethod
    def from_config(cls, input_config: dict[str, Any]) -> "SurroundingsSectionFom":
        _section = cls(
            construction_distance=SectionConfigHelper.get_float(
                input_config.get("constructieafstand", None)
            ),
            construction_buffer=SectionConfigHelper.get_float(
                input_config.get("constructieovergang", None)
            ),
            waterside=SectionConfigHelper.get_bool(input_config.get("buitendijks", None)),
            allow_waterside_reinforcement=SectionConfigHelper.get_bool(
                input_config.get("toegestaanbuitenzijdeversterking", True)
            ),
            obstacle_types={
                _type.get("type")
                .lower()
                .strip(): SectionConfigHelper.get_float_without_default(
                    _type.get("buffer", None)
                )
                for _type in input_config.get("omgevingtypes", [])
            },
        )
        return _section
