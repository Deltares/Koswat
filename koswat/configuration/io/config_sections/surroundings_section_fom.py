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
from typing import Any

from koswat.configuration.io.config_sections.config_section_helper import (
    SectionConfigHelper,
)
from koswat.core.io.json.koswat_json_fom_protocol import KoswatJsonFomProtocol


@dataclass
class SurroundingsSectionFom(KoswatJsonFomProtocol):
    construction_distance: float
    construction_buffer: float
    waterside: bool
    obstacle_types: dict[str, float] = field(default_factory=dict)

    @classmethod
    def from_config(cls, input_config: dict[str, Any]) -> "SurroundingsSectionFom":
        _section = cls(
            construction_distance=SectionConfigHelper.get_float(
                input_config["constructieafstand"]
            ),
            construction_buffer=SectionConfigHelper.get_float(
                input_config["constructieovergang"]
            ),
            waterside=SectionConfigHelper.get_bool(input_config["buitendijks"]),
            obstacle_types={
                k.lower().strip(): v
                for d in input_config.get("omgevingtypes", [])
                for k, v in d.items()
            },
        )
        return _section
