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

from __future__ import annotations

import logging
from dataclasses import dataclass
from enum import Enum

from koswat.dike.surroundings.surroundings_infrastructure import (
    SurroundingsInfrastructure,
)
from koswat.dike.surroundings.surroundings_obstacle import SurroundingsObstacle


@dataclass
class SurroundingsEnumType:
    surrounding_type: type[SurroundingsInfrastructure | SurroundingsObstacle]
    dutch_text: str = ""


class SurroundingsEnum(SurroundingsEnumType, Enum):
    # Simple format
    BUILDINGS = SurroundingsObstacle, "bebouwing"
    RAILWAYS = SurroundingsObstacle, "spoorwegen"
    WATERS = SurroundingsObstacle, "water"
    CUSTOM = SurroundingsObstacle, "custom"

    # Extended format
    ROADS_CLASS_2_POLDERSIDE = SurroundingsInfrastructure, "wegen_binnendijks_klasse2"
    ROADS_CLASS_7_POLDERSIDE = SurroundingsInfrastructure, "wegen_binnendijks_klasse7"
    ROADS_CLASS_24_POLDERSIDE = SurroundingsInfrastructure, "wegen_binnendijks_klasse24"
    ROADS_CLASS_47_POLDERSIDE = SurroundingsInfrastructure, "wegen_binnendijks_klasse47"
    ROADS_CLASS_UNKNOWN_POLDERSIDE = (
        SurroundingsInfrastructure,
        "wegen_binnendijks_klasseonbekend",
    )
    ROADS_CLASS_2_WATERSIDE = SurroundingsInfrastructure, "wegen_buitendijks_klasse2"
    ROADS_CLASS_7_WATERSIDE = SurroundingsInfrastructure, "wegen_buitendijks_klasse7"
    ROADS_CLASS_24_WATERSIDE = SurroundingsInfrastructure, "wegen_buitendijks_klasse24"
    ROADS_CLASS_47_WATERSIDE = SurroundingsInfrastructure, "wegen_buitendijks_klasse47"
    ROADS_CLASS_UNKNOWN_WATERSIDE = (
        SurroundingsInfrastructure,
        "wegen_buitendijks_klasseonbekend",
    )

    @classmethod
    def translate(cls, surrounding_type_str: str) -> SurroundingsEnum:
        """
        Translates a string representation of a surrounding type into a SurroundingsEnum.
        When not found, it defaults to CUSTOM.

        Args:
            surrounding_type_str (str): The string representation of the surrounding type.

        Returns:
            SurroundingsEnum: The corresponding SurroundingsEnum member.
        """
        normalized = surrounding_type_str.lower().strip()
        _translation = next(
            (item for item in cls if item.dutch_text == normalized), cls.CUSTOM
        )
        logging.info(
            f"Surrounding type: {surrounding_type_str} is mapped to {_translation.name.lower()}"
        )
        return _translation
