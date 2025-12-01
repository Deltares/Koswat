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
    buildings: bool
    railways: bool
    waters: bool
    custom_obstacles: list[str] = field(default_factory=list)

    @classmethod
    def from_config(cls, input_config: dict[str, Any]) -> "SurroundingsSectionFom":
        _types = [
            _type.lower().strip() for _type in input_config.get("omgevingtypes", [])
        ]

        def pop_surrounding_type(type_name: str) -> bool:
            if type_name in _types:
                _types.remove(type_name)
                return True
            return False

        _section = cls(
            construction_distance=SectionConfigHelper.get_float(
                input_config["constructieafstand"]
            ),
            construction_buffer=SectionConfigHelper.get_float(
                input_config["constructieovergang"]
            ),
            waterside=pop_surrounding_type("buitendijks"),
            buildings=pop_surrounding_type("bebouwing"),
            railways=pop_surrounding_type("spoorwegen"),
            waters=pop_surrounding_type("water"),
            custom_obstacles=[name for name in _types],
        )
        return _section
